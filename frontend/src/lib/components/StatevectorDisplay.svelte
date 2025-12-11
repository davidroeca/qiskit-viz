<script lang="ts">
  import { onMount } from 'svelte'
  import * as d3 from 'd3'
  import type { StatevectorResponse } from '$lib/api/types.gen'

  interface Props {
    statevector?: StatevectorResponse
  }

  let { statevector = $bindable() }: Props = $props()

  let container: HTMLDivElement
  let svg: d3.Selection<SVGSVGElement, unknown, null, undefined>

  onMount(() => {
    initVisualization()
  })

  $effect(() => {
    if (statevector && svg) {
      updateVisualization(statevector)
    }
  })

  function initVisualization() {
    svg = d3
      .select(container)
      .append('svg')
      .attr('width', '100%')
      .attr('height', 400)
      .style('background', '#243b53') // primary-800
      .style('border-radius', '0.5rem')
  }

  function updateVisualization(sv: StatevectorResponse) {
    const width = container.clientWidth
    const height = 400
    const margin = { top: 40, right: 20, bottom: 60, left: 60 }

    svg.selectAll('*').remove()

    const chartWidth = width - margin.left - margin.right
    const chartHeight = height - margin.top - margin.bottom

    const g = svg
      .append('g')
      .attr('transform', `translate(${margin.left},${margin.top})`)

    // Scales
    const x = d3
      .scaleBand()
      .domain(sv.basis_states)
      .range([0, chartWidth])
      .padding(0.2)

    const y = d3
      .scaleLinear()
      .domain([0, d3.max(sv.probabilities) || 1])
      .nice()
      .range([chartHeight, 0])

    // Bars for probabilities
    g.selectAll('.bar')
      .data(sv.probabilities)
      .enter()
      .append('rect')
      .attr('class', 'bar')
      .attr('x', (_d: number, i: number) => x(sv.basis_states[i]) || 0)
      .attr('y', (d: number) => y(d))
      .attr('width', x.bandwidth())
      .attr('height', (d: number) => chartHeight - y(d))
      .attr('fill', '#627d98') // primary-500
      .attr('opacity', 0.9)
      .on('mouseover', function (this: SVGRectElement) {
        d3.select(this).attr('opacity', 1).attr('fill', '#829ab1') // primary-400
      })
      .on('mouseout', function (this: SVGRectElement) {
        d3.select(this).attr('opacity', 0.9).attr('fill', '#627d98') // primary-500
      })

    // Add probability labels on bars
    g.selectAll('.label')
      .data(sv.probabilities)
      .enter()
      .append('text')
      .attr('class', 'label')
      .attr('x', (_d: number, i: number) => (x(sv.basis_states[i]) || 0) + x.bandwidth() / 2)
      .attr('y', (d: number) => y(d) - 5)
      .attr('text-anchor', 'middle')
      .attr('font-size', '12px')
      .attr('fill', '#d9e2ec') // primary-100
      .text((d: number) => d.toFixed(3))

    // X Axis
    const xAxis = g.append('g')
      .attr('transform', `translate(0,${chartHeight})`)
      .call(d3.axisBottom(x))

    xAxis.selectAll('text')
      .attr('font-size', '12px')
      .attr('font-family', 'monospace')
      .attr('fill', '#d9e2ec') // primary-100

    xAxis.selectAll('line, path')
      .attr('stroke', '#627d98') // primary-500

    // Y Axis
    const yAxis = g.append('g')
      .call(d3.axisLeft(y).ticks(5))

    yAxis.selectAll('text')
      .attr('font-size', '12px')
      .attr('fill', '#d9e2ec') // primary-100

    yAxis.selectAll('line, path')
      .attr('stroke', '#627d98') // primary-500

    // Y Axis Label
    g.append('text')
      .attr('transform', 'rotate(-90)')
      .attr('y', 0 - margin.left + 15)
      .attr('x', 0 - chartHeight / 2)
      .attr('dy', '1em')
      .style('text-anchor', 'middle')
      .attr('font-size', '14px')
      .attr('fill', '#d9e2ec') // primary-100
      .text('Probability')

    // X Axis Label
    g.append('text')
      .attr('x', chartWidth / 2)
      .attr('y', chartHeight + margin.bottom - 10)
      .style('text-anchor', 'middle')
      .attr('font-size', '14px')
      .attr('fill', '#d9e2ec') // primary-100
      .text('Basis State')

    // Title
    svg
      .append('text')
      .attr('x', width / 2)
      .attr('y', 20)
      .style('text-anchor', 'middle')
      .attr('font-size', '16px')
      .attr('font-weight', 'bold')
      .attr('fill', '#f0f4f8') // primary-50
      .text('State Probabilities')
  }
</script>

<div
  class="statevector-display rounded-xl border border-primary-600 bg-primary-800 p-6 shadow-lg"
>
  <h2 class="mb-4 text-2xl font-bold text-primary-100">Statevector</h2>

  <div bind:this={container} class="visualization-container"></div>

  {#if statevector}
    <div class="mt-6">
      <h3 class="mb-3 font-semibold text-primary-100">Amplitude Details</h3>
      <div
        class="grid max-h-60 grid-cols-2 gap-3 overflow-y-auto md:grid-cols-3 lg:grid-cols-4"
      >
        {#each statevector.basis_states as state, i}
          {@const amp = statevector.amplitudes[i]}
          {@const prob = statevector.probabilities[i]}
          <div class="rounded-lg bg-primary-700 p-3">
            <div class="mb-1 font-mono font-bold text-primary-100">|{state}⟩</div>
            <div class="text-xs text-primary-200">
              <div>Real: {amp[0].toFixed(4)}</div>
              <div>Imag: {amp[1].toFixed(4)}</div>
              <div class="mt-1 font-semibold">P: {prob.toFixed(4)}</div>
            </div>
          </div>
        {/each}
      </div>
    </div>
  {/if}
</div>

<style>
  .visualization-container {
    width: 100%;
    min-height: 400px;
  }
</style>
