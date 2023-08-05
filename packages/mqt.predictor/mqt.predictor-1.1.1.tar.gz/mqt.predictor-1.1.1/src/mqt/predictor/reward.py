from qiskit import QuantumCircuit

from mqt.predictor import Calibration
from mqt.predictor.utils import (
    calc_qubit_index,
    calc_supermarq_features,
    get_rigetti_qubit_dict,
)


def crit_depth(qc):
    (
        program_communication,
        critical_depth,
        entanglement_ratio,
        parallelism,
        liveness,
    ) = calc_supermarq_features(qc)
    return 1 - critical_depth


def parallelism(qc):
    (
        program_communication,
        critical_depth,
        entanglement_ratio,
        parallelism,
        liveness,
    ) = calc_supermarq_features(qc)
    return critical_depth


def expected_fidelity(qc_or_path: str, device: str):
    if isinstance(qc_or_path, QuantumCircuit):
        qc = qc_or_path
    else:
        try:
            qc = QuantumCircuit.from_qasm_file(qc_or_path)
        except Exception as e:
            print("Fail in reward_expected_fidelity reading a the quantum circuit: ", e)
            return 0
    res = 1

    calibration = Calibration.Calibration()

    if "ibm_montreal" in device or "ibm_washington" in device:

        if "ibm_montreal" in device:
            backend = calibration.ibm_montreal_calibration
        else:
            backend = calibration.ibm_washington_calibration

        for instruction, qargs, _cargs in qc.data:
            gate_type = instruction.name

            assert gate_type in ["rz", "sx", "x", "cx", "measure", "barrier"]

            if gate_type != "barrier":
                assert len(qargs) in [1, 2]
                first_qubit = calc_qubit_index(qargs, qc.qregs, 0)
                if len(qargs) == 1:
                    try:
                        if gate_type == "measure":
                            specific_error = backend.readout_error(first_qubit)
                        else:
                            specific_error = backend.gate_error(
                                gate_type, [first_qubit]
                            )
                    except Exception as e:
                        print(instruction, qargs)
                        print(
                            "Error in IBM backend.gate_error(): ",
                            e,
                            device,
                            first_qubit,
                        )
                        return 0
                else:
                    second_qubit = calc_qubit_index(qargs, qc.qregs, 1)
                    try:
                        specific_error = backend.gate_error(
                            gate_type, [first_qubit, second_qubit]
                        )
                        if specific_error == 1:
                            specific_error = calibration.ibm_washington_cx_mean_error
                    except Exception as e:
                        print(instruction, qargs)
                        print(
                            "Error in IBM backend.gate_error(): ",
                            e,
                            device,
                            first_qubit,
                            second_qubit,
                        )
                        return 0

                res *= 1 - float(specific_error)
    elif "oqc_lucy" in device:
        for instruction, qargs, _cargs in qc.data:
            gate_type = instruction.name

            assert gate_type in ["rz", "sx", "x", "ecr", "measure", "barrier"]
            if gate_type != "barrier":
                assert len(qargs) in [1, 2]
                first_qubit = calc_qubit_index(qargs, qc.qregs, 0)
                if len(qargs) == 1 and gate_type != "measure":
                    specific_fidelity = calibration.oqc_lucy_calibration["fid_1Q"][
                        str(first_qubit)
                    ]
                elif len(qargs) == 1 and gate_type == "measure":
                    specific_fidelity = calibration.oqc_lucy_calibration[
                        "fid_1Q_readout"
                    ][str(first_qubit)]
                elif len(qargs) == 2:
                    second_qubit = calc_qubit_index(qargs, qc.qregs, 1)
                    tmp = str(first_qubit) + "-" + str(second_qubit)
                    if calibration.oqc_lucy_calibration["fid_2Q"].get(tmp) is None:
                        specific_fidelity = calibration.oqc_lucy_calibration["avg_2Q"]
                    else:
                        specific_fidelity = calibration.oqc_lucy_calibration["fid_2Q"][
                            tmp
                        ]

                res *= specific_fidelity

    elif "ionq11" in device:
        for instruction, qargs, _cargs in qc.data:
            gate_type = instruction.name

            assert gate_type in ["rxx", "rz", "ry", "rx", "measure", "barrier"]
            if gate_type != "barrier":
                assert len(qargs) in [1, 2]

                if len(qargs) == 1:
                    specific_fidelity = calibration.ionq_calibration["avg_1Q"]
                elif len(qargs) == 2:
                    specific_fidelity = calibration.ionq_calibration["avg_2Q"]
                res *= specific_fidelity
    elif "rigetti_aspen_m2" in device:

        mapping = get_rigetti_qubit_dict()
        for instruction, qargs, _cargs in qc.data:
            gate_type = instruction.name

            assert gate_type in ["rx", "rz", "cz", "measure", "barrier"]
            if gate_type != "barrier":
                assert len(qargs) in [1, 2]
                first_qubit = calc_qubit_index(qargs, qc.qregs, 0)
                if len(qargs) == 1:
                    if gate_type == "measure":
                        specific_fidelity = calibration.rigetti_m2_calibration[
                            "fid_1Q_readout"
                        ][mapping.get(str(first_qubit))]
                    else:
                        specific_fidelity = calibration.rigetti_m2_calibration[
                            "fid_1Q"
                        ][mapping.get(str(first_qubit))]
                else:
                    second_qubit = calc_qubit_index(qargs, qc.qregs, 1)
                    tmp = (
                        str(
                            min(
                                int(mapping.get(str(first_qubit))),
                                int(mapping.get(str(second_qubit))),
                            )
                        )
                        + "-"
                        + str(
                            max(
                                int(mapping.get(str(first_qubit))),
                                int(mapping.get(str(second_qubit))),
                            )
                        )
                    )
                    if (
                        calibration.rigetti_m2_calibration["fid_2Q_CZ"].get(tmp) is None
                        or calibration.rigetti_m2_calibration["fid_2Q_CZ"][tmp] is None
                    ):
                        specific_fidelity = calibration.rigetti_m2_calibration["avg_2Q"]
                    else:
                        specific_fidelity = calibration.rigetti_m2_calibration[
                            "fid_2Q_CZ"
                        ][tmp]

                res *= specific_fidelity

    else:
        print("Error: No suitable backend found!")

    return res
