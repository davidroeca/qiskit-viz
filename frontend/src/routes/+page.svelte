<script lang="ts">
  import CircuitBuilder from '$lib/components/CircuitBuilder.svelte'
  import BlochSphere from '$lib/components/BlochSphere.svelte'
  import StatevectorDisplay from '$lib/components/StatevectorDisplay.svelte'
  import { Play, Minus, Plus } from 'lucide-svelte'
  import type {
    GateOperation,
    StatevectorResponse,
    BlochVectorResponse,
    CircuitResponse,
  } from '$lib/api/types.gen'
  import {
    buildCircuitV1CircuitBuildPost,
    getStatevectorV1CircuitStatevectorPost,
    getBlochVectorV1BlochQubitPost,
  } from '$lib/api/sdk.gen'

  let numQubits = $state(2)
  let operations = $state<GateOperation[]>([])
  let circuitInfo = $state<CircuitResponse | undefined>()
  let statevector = $state<StatevectorResponse | undefined>()
  let blochVector = $state<BlochVectorResponse | undefined>()
  let selectedQubitForBloch = $state(0)
  let errorMessage = $state<string | undefined>()
  let isLoading = $state(false)

  async function executeCircuit() {
    if (operations.length === 0) {
      errorMessage = 'Please add at least one gate operation'
      return
    }

    isLoading = true
    errorMessage = undefined

    try {
      const circuitRequest = {
        num_qubits: numQubits,
        operations: operations,
      }

      // Build circuit and get metadata
      const circuitResponse = await buildCircuitV1CircuitBuildPost({
        body: circuitRequest,
      })

      if (circuitResponse.data) {
        circuitInfo = circuitResponse.data
      }

      // Get statevector
      const svResponse = await getStatevectorV1CircuitStatevectorPost({
        body: circuitRequest,
      })

      if (svResponse.data) {
        statevector = svResponse.data
      }

      // Get Bloch vector for selected qubit
      const blochResponse = await getBlochVectorV1BlochQubitPost({
        path: { qubit: selectedQubitForBloch },
        body: circuitRequest,
      })

      if (blochResponse.data) {
        blochVector = blochResponse.data
      }
    } catch (error) {
      errorMessage =
        error instanceof Error ? error.message : 'An error occurred'
      console.error('Error executing circuit:', error)
    } finally {
      isLoading = false
    }
  }

  function handleOperationsChange(ops: GateOperation[]) {
    operations = ops
  }
</script>

<div class="min-h-screen bg-gradient-to-br from-primary-900 to-primary-800 p-6">
  <div class="mx-auto max-w-7xl">
    <header class="mb-8 text-center">
      <h1 class="mb-2 text-5xl font-bold text-primary-50">Qiskit Viz</h1>
      <p class="text-xl text-primary-200">
        Interactive Quantum Circuit Visualization with Svelte & Three.js
      </p>
    </header>

    {#if errorMessage}
      <div
        class="mb-6 rounded-lg border-l-4 border-danger-600 bg-danger-600/10 p-4 text-danger-600"
        role="alert"
      >
        <p class="font-semibold">Error</p>
        <p>{errorMessage}</p>
      </div>
    {/if}

    <div class="mb-6 grid gap-6">
      <div class="rounded-xl border border-primary-600 bg-primary-800 p-6 shadow-lg">
        <div class="mb-4 flex items-center justify-between">
          <div>
            <label for="num-qubits" class="mb-2 block text-sm font-medium text-primary-100"
              >Number of Qubits</label
            >
            <div class="flex items-center gap-2">
              <button
                onclick={() => numQubits = Math.max(1, numQubits - 1)}
                class="cursor-pointer rounded-lg bg-primary-600 p-2 text-primary-100 transition-colors hover:bg-primary-500"
                aria-label="Decrease qubits"
              >
                <Minus size={16} />
              </button>
              <input
                id="num-qubits"
                type="number"
                min="1"
                max="5"
                bind:value={numQubits}
                class="w-16 rounded-lg border border-primary-500 bg-primary-700 p-2 text-center text-primary-100 [appearance:textfield] [&::-webkit-inner-spin-button]:appearance-none [&::-webkit-outer-spin-button]:appearance-none"
              />
              <button
                onclick={() => numQubits = Math.min(5, numQubits + 1)}
                class="cursor-pointer rounded-lg bg-primary-600 p-2 text-primary-100 transition-colors hover:bg-primary-500"
                aria-label="Increase qubits"
              >
                <Plus size={16} />
              </button>
            </div>
          </div>

          <div>
            <label for="bloch-qubit" class="mb-2 block text-sm font-medium text-primary-100"
              >Bloch Sphere Qubit</label
            >
            <select
              id="bloch-qubit"
              bind:value={selectedQubitForBloch}
              class="rounded-lg border border-primary-500 bg-primary-700 p-2 text-primary-100"
            >
              {#each Array(numQubits) as _, i}
                <option value={i}>Qubit {i}</option>
              {/each}
            </select>
          </div>

          <button
            onclick={executeCircuit}
            disabled={isLoading}
            class="cursor-pointer rounded-xl bg-execute-600 px-6 py-3 font-bold text-white transition-colors hover:bg-execute-700 disabled:cursor-not-allowed disabled:bg-primary-400"
          >
            <span class="flex items-center gap-2">
              {#if isLoading}
                <svg
                  class="h-5 w-5 animate-spin"
                  xmlns="http://www.w3.org/2000/svg"
                  fill="none"
                  viewBox="0 0 24 24"
                >
                  <circle
                    class="opacity-25"
                    cx="12"
                    cy="12"
                    r="10"
                    stroke="currentColor"
                    stroke-width="4"
                  ></circle>
                  <path
                    class="opacity-75"
                    fill="currentColor"
                    d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
                  ></path>
                </svg>
                Executing...
              {:else}
                <Play size={20} fill="currentColor" />
                Execute Circuit
              {/if}
            </span>
          </button>
        </div>
      </div>

      <CircuitBuilder
        {numQubits}
        bind:operations
        onOperationsChange={handleOperationsChange}
      />

      {#if circuitInfo}
        <div class="rounded-xl border border-primary-600 bg-primary-800 p-6 shadow-lg">
          <h2 class="mb-4 text-2xl font-bold text-primary-100">Circuit Information</h2>
          <div class="grid gap-4 md:grid-cols-2">
            <div class="text-primary-200">
              <span class="font-semibold">Depth:</span>
              <span class="ml-2">{circuitInfo.depth}</span>
            </div>
            <div class="text-primary-200">
              <span class="font-semibold">Qubits:</span>
              <span class="ml-2">{circuitInfo.num_qubits}</span>
            </div>
          </div>
          <div class="mt-4">
            <h3 class="mb-2 font-semibold text-primary-100">QASM:</h3>
            <pre
              class="overflow-x-auto rounded-lg bg-primary-900 p-4 font-mono text-sm text-primary-200">{circuitInfo.qasm}</pre>
          </div>
        </div>
      {/if}
    </div>

    <div class="grid gap-6 lg:grid-cols-2">
      <BlochSphere {blochVector} />
      <StatevectorDisplay {statevector} />
    </div>
  </div>
</div>
