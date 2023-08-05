import sys

import numpy as np
from pytket import architecture
from pytket.circuit import OpType
from pytket.passes import (
    CliffordSimp,
    DecomposeMultiQubitsCX,
    FullPeepholeOptimise,
    PeepholeOptimise2Q,
    RemoveRedundancies,
    RoutingPass,
)
from qiskit import QuantumCircuit
from qiskit.circuit.equivalence_library import StandardEquivalenceLibrary
from qiskit.circuit.library import XGate, ZGate
from qiskit.providers.fake_provider import FakeMontreal, FakeWashington
from qiskit.transpiler import CouplingMap
from qiskit.transpiler.passes import (
    ApplyLayout,
    BasicSwap,
    BasisTranslator,
    Collect2qBlocks,
    CommutativeCancellation,
    CommutativeInverseCancellation,
    ConsolidateBlocks,
    CXCancellation,
    DenseLayout,
    EnlargeWithAncilla,
    FullAncillaAllocation,
    InverseCancellation,
    Optimize1qGatesDecomposition,
    OptimizeCliffords,
    RemoveDiagonalGatesBeforeMeasure,
    SabreLayout,
    SabreSwap,
    StochasticSwap,
    TrivialLayout,
)

from mqt.predictor import utils

if sys.version_info < (3, 10, 0):
    import importlib_resources as resources
else:
    from importlib import resources


def get_actions_opt():
    return [
        {
            "name": "Optimize1qGatesDecomposition",
            "transpile_pass": [Optimize1qGatesDecomposition()],
            "origin": "qiskit",
        },
        {
            "name": "CXCancellation",
            "transpile_pass": [CXCancellation()],
            "origin": "qiskit",
        },
        {
            "name": "CommutativeCancellation",
            "transpile_pass": [CommutativeCancellation()],
            "origin": "qiskit",
        },
        {
            "name": "CommutativeInverseCancellation",
            "transpile_pass": [CommutativeInverseCancellation()],
            "origin": "qiskit",
        },
        {
            "name": "RemoveDiagonalGatesBeforeMeasure",
            "transpile_pass": [RemoveDiagonalGatesBeforeMeasure()],
            "origin": "qiskit",
        },
        {
            "name": "InverseCancellation",
            "transpile_pass": [InverseCancellation([XGate(), ZGate()])],
            "origin": "qiskit",
        },
        {
            "name": "OptimizeCliffords",
            "transpile_pass": [OptimizeCliffords()],
            "origin": "qiskit",
        },
        {
            "name": "Opt2qBlocks",
            "transpile_pass": [Collect2qBlocks(), ConsolidateBlocks()],
            "origin": "qiskit",
        },
        {
            "name": "PeepholeOptimise2Q",
            "transpile_pass": [PeepholeOptimise2Q()],
            "origin": "tket",
        },
        {
            "name": "CliffordSimp",
            "transpile_pass": [CliffordSimp()],
            "origin": "tket",
        },
        {
            "name": "FullPeepholeOptimiseCX",
            "transpile_pass": [FullPeepholeOptimise(target_2qb_gate=OpType.TK2)],
            "origin": "tket",
        },
        {
            "name": "RemoveRedundancies",
            "transpile_pass": [RemoveRedundancies()],
            "origin": "tket",
        },
    ]


def get_actions_layout():
    return [
        {
            "name": "TrivialLayout",
            "transpile_pass": lambda c: [
                TrivialLayout(coupling_map=CouplingMap(c)),
                FullAncillaAllocation(coupling_map=CouplingMap(c)),
                EnlargeWithAncilla(),
                ApplyLayout(),
            ],
            "origin": "qiskit",
        },
        {
            "name": "DenseLayout",
            "transpile_pass": lambda c: [
                DenseLayout(coupling_map=CouplingMap(c)),
                FullAncillaAllocation(coupling_map=CouplingMap(c)),
                EnlargeWithAncilla(),
                ApplyLayout(),
            ],
            "origin": "qiskit",
        },
        {
            "name": "SabreLayout_IBM_washington",
            "transpile_pass": lambda c: [
                SabreLayout(coupling_map=CouplingMap(c)),
                FullAncillaAllocation(coupling_map=CouplingMap(c)),
                EnlargeWithAncilla(),
                ApplyLayout(),
            ],
            "origin": "qiskit",
        },
    ]


def get_actions_routing():
    return [
        {
            "name": "BasicSwap",
            "transpile_pass": lambda c: [BasicSwap(coupling_map=CouplingMap(c))],
            "origin": "qiskit",
        },
        {
            "name": "RoutingPass",
            "transpile_pass": lambda c: [
                RoutingPass(architecture.Architecture(c)),
                DecomposeMultiQubitsCX(),
            ],
            "origin": "tket",
        },
        {
            "name": "StochasticSwap",
            "transpile_pass": lambda c: [StochasticSwap(coupling_map=CouplingMap(c))],
            "origin": "qiskit",
        },
        {
            "name": "SabreSwap",
            "transpile_pass": lambda c: [SabreSwap(coupling_map=CouplingMap(c))],
            "origin": "qiskit",
        },
    ]


def get_actions_platform_selection():
    return [
        {
            "name": "IBM",
            "gates": get_ibm_native_gates(),
            "devices": ["ibm_washington", "ibm_montreal"],
            "max_qubit_size": 127,
        },
        {
            "name": "Rigetti",
            "gates": get_rigetti_native_gates(),
            "devices": ["rigetti_aspen_m2"],
            "max_qubit_size": 80,
        },
        {
            "name": "OQC",
            "gates": get_oqc_native_gates(),
            "devices": ["oqc_lucy"],
            "max_qubit_size": 8,
        },
        {
            "name": "IonQ",
            "gates": get_ionq_native_gates(),
            "devices": ["ionq11"],
            "max_qubit_size": 11,
        },
    ]


def get_actions_synthesis():
    return [
        {
            "name": "BasisTranslator",
            "transpile_pass": lambda g: [
                BasisTranslator(StandardEquivalenceLibrary, target_basis=g)
            ],
            "origin": "qiskit",
        },
    ]


def get_action_terminate():
    return {"name": "terminate"}


def get_actions_devices():
    return [
        {
            "name": "ibm_washington",
            "transpile_pass": [],
            "full_connectivity": False,
            "cmap": get_cmap_from_devicename("ibm_washington"),
            "max_qubits": 127,
        },
        {
            "name": "ibm_montreal",
            "transpile_pass": [],
            "device": "ibm_montreal",
            "full_connectivity": False,
            "cmap": get_cmap_from_devicename("ibm_montreal"),
            "max_qubits": 27,
        },
        {
            "name": "oqc_lucy",
            "transpile_pass": [],
            "device": "oqc_lucy",
            "full_connectivity": False,
            "cmap": get_cmap_from_devicename("oqc_lucy"),
            "max_qubits": 8,
        },
        {
            "name": "rigetti_aspen_m2",
            "transpile_pass": [],
            "device": "rigetti_aspen_m2",
            "full_connectivity": False,
            "cmap": get_cmap_from_devicename("rigetti_aspen_m2"),
            "max_qubits": 80,
        },
        {
            "name": "ionq11",
            "transpile_pass": [],
            "device": "ionq11",
            "full_connectivity": True,
            "cmap": get_cmap_from_devicename("ionq11"),
            "max_qubits": 11,
        },
    ]


def get_random_state_sample():
    file_list = list(get_path_training_circuits().glob("*.qasm"))

    path_zip = get_path_training_circuits() / "mqtbench_sample_circuits.zip"
    if len(file_list) == 0 and path_zip.exists():
        path_zip = str(path_zip)
        import zipfile

        with zipfile.ZipFile(path_zip, "r") as zip_ref:
            zip_ref.extractall(get_path_training_circuits())

        file_list = list(get_path_training_circuits().glob("*.qasm"))
        assert len(file_list) > 0

    random_index = np.random.randint(len(file_list))
    try:
        qc = QuantumCircuit.from_qasm_file(str(file_list[random_index]))
    except Exception:
        print("ERROR: ", file_list[random_index])
        return False
    return qc


def get_ibm_native_gates():
    ibm_gates = ["rz", "sx", "x", "cx", "measure"]
    return ibm_gates


def get_rigetti_native_gates():
    rigetti_gates = ["rx", "rz", "cz", "measure"]
    return rigetti_gates


def get_ionq_native_gates():
    ionq_gates = ["rxx", "rz", "ry", "rx", "measure"]
    return ionq_gates


def get_oqc_native_gates():
    oqc_gates = ["rz", "sx", "x", "ecr", "measure"]
    return oqc_gates


def get_rigetti_aspen_m2_map():
    """Returns a coupling map of Rigetti Aspen M2 chip."""
    c_map_rigetti = []
    for j in range(5):
        for i in range(0, 7):
            c_map_rigetti.append([i + j * 8, i + 1 + j * 8])

            if i == 6:
                c_map_rigetti.append([0 + j * 8, 7 + j * 8])

        if j != 0:
            c_map_rigetti.append([j * 8 - 6, j * 8 + 5])
            c_map_rigetti.append([j * 8 - 7, j * 8 + 6])

    for j in range(5):
        m = 8 * j + 5 * 8
        for i in range(0, 7):
            c_map_rigetti.append([i + m, i + 1 + m])

            if i == 6:
                c_map_rigetti.append([0 + m, 7 + m])

        if j != 0:
            c_map_rigetti.append([m - 6, m + 5])
            c_map_rigetti.append([m - 7, m + 6])

    for n in range(5):
        c_map_rigetti.append([n * 8 + 3, n * 8 + 5 * 8])
        c_map_rigetti.append([n * 8 + 4, n * 8 + 7 + 5 * 8])

    inverted = [[item[1], item[0]] for item in c_map_rigetti]
    c_map_rigetti = c_map_rigetti + inverted

    return c_map_rigetti


def get_ionq11_c_map():
    ionq11_c_map = []
    for i in range(0, 11):
        for j in range(0, 11):
            if i != j:
                ionq11_c_map.append([i, j])
    return ionq11_c_map


def get_cmap_oqc_lucy():
    """Returns the coupling map of the OQC Lucy quantum computer."""
    # source: https://github.com/aws/amazon-braket-examples/blob/main/examples/braket_features/Verbatim_Compilation.ipynb

    # Connections are NOT bidirectional, this is not an accident
    c_map_oqc_lucy = [[0, 1], [0, 7], [1, 2], [2, 3], [7, 6], [6, 5], [4, 3], [4, 5]]

    return c_map_oqc_lucy


def get_cmap_from_devicename(device: str):
    if device == "ibm_washington":
        return FakeWashington().configuration().coupling_map
    elif device == "ibm_montreal":
        return FakeMontreal().configuration().coupling_map
    elif device == "rigetti_aspen_m2":
        return get_rigetti_aspen_m2_map()
    elif device == "oqc_lucy":
        return get_cmap_oqc_lucy()
    elif device == "ionq11":
        return get_ionq11_c_map()
    else:
        raise ValueError("Unknown device name")


def create_feature_dict(qc):
    feature_dict = {"num_qubits": qc.num_qubits, "depth": qc.depth()}

    (
        program_communication,
        critical_depth,
        entanglement_ratio,
        parallelism,
        liveness,
    ) = utils.calc_supermarq_features(qc)
    feature_dict["program_communication"] = int(program_communication * 100)
    feature_dict["critical_depth"] = int(critical_depth * 100)
    feature_dict["entanglement_ratio"] = int(entanglement_ratio * 100)
    feature_dict["parallelism"] = int(parallelism * 100)
    feature_dict["liveness"] = int(liveness * 100)

    return feature_dict


def get_path_training_data():
    return resources.files("mqt.predictor") / "rl" / "training_data"


def get_path_trained_model():
    return get_path_training_data() / "trained_model"


def get_path_training_circuits():
    return get_path_training_data() / "training_circuits"
