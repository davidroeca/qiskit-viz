"""Quantum circuit operations using Qiskit."""

import numpy as np
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector, partial_trace

from .schemas import GateOperation


def apply_gates_to_circuit(
    qc: QuantumCircuit, operations: list[GateOperation], num_qubits: int
) -> None:
    """Apply gate operations to a quantum circuit.

    Args:
        qc: Quantum circuit to modify
        operations: List of gate operations to apply
        num_qubits: Total number of qubits in circuit

    Raises:
        ValueError: If qubit index is out of range or gate is unsupported
    """
    for op in operations:
        gate = op.gate.lower()
        qubit = op.qubit

        if qubit >= num_qubits:
            raise ValueError(f"Qubit index {qubit} out of range")

        # Single-qubit gates
        if gate == "h":
            qc.h(qubit)
        elif gate == "x":
            qc.x(qubit)
        elif gate == "y":
            qc.y(qubit)
        elif gate == "z":
            qc.z(qubit)
        elif gate == "s":
            qc.s(qubit)
        elif gate == "t":
            qc.t(qubit)
        elif gate == "sdg":
            qc.sdg(qubit)
        elif gate == "tdg":
            qc.tdg(qubit)
        elif gate == "rx" and len(op.params) >= 1:
            qc.rx(op.params[0], qubit)
        elif gate == "ry" and len(op.params) >= 1:
            qc.ry(op.params[0], qubit)
        elif gate == "rz" and len(op.params) >= 1:
            qc.rz(op.params[0], qubit)
        else:
            raise ValueError(f"Unsupported gate: {gate}")


def calculate_bloch_vector(
    num_qubits: int, operations: list[GateOperation], target_qubit: int
) -> tuple[float, float, float]:
    """Calculate Bloch sphere coordinates for a specific qubit.

    Args:
        num_qubits: Number of qubits in circuit
        operations: List of gate operations
        target_qubit: Qubit to calculate Bloch vector for

    Returns:
        Tuple of (x, y, z) Bloch vector coordinates

    Raises:
        ValueError: If qubit index is out of range
    """
    if target_qubit >= num_qubits:
        raise ValueError(f"Qubit index {target_qubit} out of range")

    qc = QuantumCircuit(num_qubits)
    apply_gates_to_circuit(qc, operations, num_qubits)

    # Get statevector and extract single qubit density matrix
    sv = Statevector(qc)

    # For a single qubit, get the density matrix directly
    # For multi-qubit systems, use partial trace on the statevector
    if num_qubits == 1:
        density_matrix = sv.to_operator().to_matrix()
    else:
        # Partial trace to get single qubit state
        # Trace out all qubits except the target
        qubits_to_trace = [i for i in range(num_qubits) if i != target_qubit]
        reduced_rho = partial_trace(sv, qubits_to_trace)
        density_matrix = reduced_rho.data

    # Calculate Bloch vector from density matrix
    # rho = (I + r*sigma) / 2, where r is the Bloch vector
    # r_x = Tr(rho * sigma_x), r_y = Tr(rho * sigma_y), r_z = Tr(rho * sigma_z)
    pauli_x = np.array([[0, 1], [1, 0]], dtype=complex)
    pauli_y = np.array([[0, -1j], [1j, 0]], dtype=complex)
    pauli_z = np.array([[1, 0], [0, -1]], dtype=complex)

    x = float(np.trace(density_matrix @ pauli_x).real)
    y = float(np.trace(density_matrix @ pauli_y).real)
    z = float(np.trace(density_matrix @ pauli_z).real)

    return (x, y, z)
