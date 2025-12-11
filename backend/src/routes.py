"""API route handlers."""

import logging
from fastapi import APIRouter, HTTPException
from qiskit import QuantumCircuit, qasm2
from qiskit.quantum_info import Statevector

from .schemas import (
    CircuitRequest,
    CircuitResponse,
    StatevectorResponse,
    BlochVectorResponse,
)
from .quantum import apply_gates_to_circuit, calculate_bloch_vector

router = APIRouter(prefix="/v1")

LOGGER = logging.getLogger(__name__)


@router.post("/circuit/build", response_model=CircuitResponse)
def build_circuit(request: CircuitRequest):
    """Build a quantum circuit from gate operations."""
    try:
        qc = QuantumCircuit(request.num_qubits)
        apply_gates_to_circuit(qc, request.operations, request.num_qubits)

        return CircuitResponse(
            qasm=qasm2.dumps(qc),
            depth=qc.depth(),
            num_qubits=qc.num_qubits,
        )

    except Exception as e:
        LOGGER.error("Something went wrong", exc_info=True)
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/circuit/statevector", response_model=StatevectorResponse)
def get_statevector(request: CircuitRequest):
    """Execute circuit and return the statevector."""
    try:
        qc = QuantumCircuit(request.num_qubits)
        apply_gates_to_circuit(qc, request.operations, request.num_qubits)

        # Get statevector
        sv = Statevector(qc)
        data = sv.data

        # Convert to serializable format
        amplitudes = [(float(z.real), float(z.imag)) for z in data]
        probabilities = [float(p) for p in sv.probabilities()]
        basis_states = [format(i, f"0{request.num_qubits}b") for i in range(len(data))]

        return StatevectorResponse(
            amplitudes=amplitudes,
            probabilities=probabilities,
            basis_states=basis_states,
        )

    except Exception as e:
        LOGGER.error("Something went wrong", exc_info=True)
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/bloch/{qubit}", response_model=BlochVectorResponse)
def get_bloch_vector(qubit: int, request: CircuitRequest):
    """Get Bloch sphere coordinates for a specific qubit."""
    try:
        x, y, z = calculate_bloch_vector(request.num_qubits, request.operations, qubit)
        return BlochVectorResponse(x=x, y=y, z=z, qubit=qubit)

    except Exception as e:
        LOGGER.error("Something went wrong", exc_info=True)
        raise HTTPException(status_code=400, detail=str(e))
