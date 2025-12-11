<script lang="ts">
  import { ArrowRight, Plus, Trash2 } from 'lucide-svelte'
  import type { GateOperation } from '$lib/api/types.gen'

  interface Props {
    numQubits?: number
    operations?: GateOperation[]
    onOperationsChange?: (ops: GateOperation[]) => void
  }

  let {
    numQubits = 2,
    operations = $bindable([]),
    onOperationsChange,
  }: Props = $props()

  const availableGates = ['H', 'X', 'Y', 'Z', 'S', 'T', 'Sdg', 'Tdg']
  const parametricGates = ['RX', 'RY', 'RZ']

  let selectedGate = $state('H')
  let selectedQubit = $state(0)
  let rotationAngle = $state(Math.PI / 2)

  function addGate() {
    const newOp: GateOperation = {
      gate: selectedGate,
      qubit: selectedQubit,
      params: parametricGates.includes(selectedGate) ? [rotationAngle] : [],
    }

    operations = [...operations, newOp]
    onOperationsChange?.(operations)
  }

  function removeGate(index: number) {
    operations = operations.filter((_, i) => i !== index)
    onOperationsChange?.(operations)
  }

  function clearCircuit() {
    operations = []
    onOperationsChange?.(operations)
  }
</script>

<div
  class="circuit-builder rounded-xl border border-primary-600 bg-primary-800 p-6 shadow-lg"
>
  <h2 class="mb-4 text-2xl font-bold text-primary-100">Circuit Builder</h2>

  <div class="mb-4">
    <p class="mb-2 block text-sm font-medium text-primary-200">Number of Qubits: {numQubits}</p>
  </div>

  <div class="grid grid-cols-1 gap-4 md:grid-cols-3">
    <div>
      <label for="gate-select" class="mb-2 block text-sm font-medium text-primary-100">
        Gate
      </label>
      <select
        id="gate-select"
        bind:value={selectedGate}
        class="w-full rounded-lg border border-primary-500 bg-primary-700 p-2 text-primary-100"
      >
        {#each availableGates as gate}
          <option value={gate}>{gate}</option>
        {/each}
        {#each parametricGates as gate}
          <option value={gate}>{gate}</option>
        {/each}
      </select>
    </div>

    <div>
      <label for="qubit-select" class="mb-2 block text-sm font-medium text-primary-100"
        >Qubit</label
      >
      <select
        id="qubit-select"
        bind:value={selectedQubit}
        class="w-full rounded-lg border border-primary-500 bg-primary-700 p-2 text-primary-100"
      >
        {#each Array(numQubits) as _, i}
          <option value={i}>q{i}</option>
        {/each}
      </select>
    </div>

    {#if parametricGates.includes(selectedGate)}
      <div>
        <label for="angle-input" class="mb-2 block text-sm font-medium text-primary-100"
          >Angle (radians): {rotationAngle.toFixed(3)}</label
        >
        <input
          id="angle-input"
          type="range"
          min="0"
          max={Math.PI * 2}
          step="0.01"
          bind:value={rotationAngle}
          class="w-full accent-primary-500"
        />
      </div>
    {/if}
  </div>

  <div class="mt-4 flex gap-2">
    <button
      onclick={addGate}
      class="cursor-pointer rounded-xl bg-primary-600 px-4 py-2 font-medium text-white transition-colors hover:bg-primary-700"
    >
      <span class="flex items-center gap-2">
        <Plus size={16} />
        Add Gate
      </span>
    </button>
    <button
      onclick={clearCircuit}
      class="cursor-pointer rounded-xl bg-danger-600 px-4 py-2 font-medium text-white transition-colors hover:bg-danger-700"
    >
      <span class="flex items-center gap-2">
        <Trash2 size={16} />
        Clear Circuit
      </span>
    </button>
  </div>

  <div class="mt-6">
    <h3 class="mb-3 text-lg font-semibold text-primary-100">Circuit Operations</h3>
    {#if operations.length === 0}
      <p class="text-primary-300">
        No operations yet. Add gates to build your circuit.
      </p>
    {:else}
      <div class="space-y-2">
        {#each operations as op, i}
          <div
            class="flex items-center justify-between rounded-lg bg-primary-700 p-3 transition-colors hover:bg-primary-600"
          >
            <span class="inline-flex items-center font-mono text-primary-100">
              {op.gate}
              {#if op.params && op.params.length > 0}
                ({op.params.map((p) => p.toFixed(3)).join(', ')})
              {/if}
              <ArrowRight size="1em" /> q{op.qubit}
            </span>
            <button
              onclick={() => removeGate(i)}
              class="cursor-pointer rounded-lg bg-danger-600 px-3 py-1 text-sm text-white transition-colors hover:bg-danger-700"
            >
              <span class="flex items-center gap-1">
                <Trash2 size={14} />
                Remove
              </span>
            </button>
          </div>
        {/each}
      </div>
    {/if}
  </div>
</div>
