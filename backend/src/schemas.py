"""Pydantic schemas for API request/response validation."""

from pydantic import BaseModel, Field


class GateOperation(BaseModel):
    gate: str
    qubit: int
    params: list[float] = Field(default_factory=lambda: [])


class CircuitRequest(BaseModel):
    num_qubits: int
    operations: list[GateOperation]


class CircuitResponse(BaseModel):
    qasm: str
    depth: int
    num_qubits: int


class StatevectorResponse(BaseModel):
    amplitudes: list[tuple[float, float]]  # (real, imag) pairs
    probabilities: list[float]
    basis_states: list[str]


class BlochVectorResponse(BaseModel):
    x: float
    y: float
    z: float
    qubit: int


class RootResponse(BaseModel):
    message: str
    api_prefix: str
    endpoints: list[str]
