<script lang="ts">
  import { onMount } from 'svelte'
  import * as THREE from 'three'
  import { OrbitControls } from 'three/addons/controls/OrbitControls.js'
  import type { BlochVectorResponse } from '$lib/api/types.gen'

  interface Props {
    blochVector?: BlochVectorResponse
  }

  let { blochVector = $bindable() }: Props = $props()

  let container: HTMLDivElement
  let scene: THREE.Scene
  let camera: THREE.PerspectiveCamera
  let renderer: THREE.WebGLRenderer
  let controls: OrbitControls
  let stateVector: THREE.ArrowHelper
  let animationId: number

  onMount(() => {
    initThreeJS()
    createBlochSphere()
    animate()

    return () => {
      if (animationId) cancelAnimationFrame(animationId)
      controls?.dispose()
      renderer?.dispose()
    }
  })

  $effect(() => {
    console.log('Bloch effect triggered:', { blochVector, stateVectorExists: !!stateVector })
    if (blochVector && stateVector) {
      updateStateVector(blochVector)
    }
  })

  function initThreeJS() {
    scene = new THREE.Scene()
    scene.background = new THREE.Color(0x243b53) // primary-800

    camera = new THREE.PerspectiveCamera(
      75,
      container.clientWidth / container.clientHeight,
      0.1,
      1000,
    )
    camera.position.set(2, 2, 2)
    camera.lookAt(0, 0, 0)

    renderer = new THREE.WebGLRenderer({ antialias: true })
    renderer.setSize(container.clientWidth, container.clientHeight)
    container.appendChild(renderer.domElement)

    // Add OrbitControls for interactive rotation
    controls = new OrbitControls(camera, renderer.domElement)
    controls.enableDamping = true
    controls.dampingFactor = 0.05
    controls.rotateSpeed = 0.5
    controls.enableZoom = true
    controls.enablePan = false

    const ambientLight = new THREE.AmbientLight(0xffffff, 0.6)
    scene.add(ambientLight)

    const directionalLight = new THREE.DirectionalLight(0xffffff, 0.8)
    directionalLight.position.set(5, 5, 5)
    scene.add(directionalLight)
  }

  function createBlochSphere() {
    // Create transparent sphere
    const sphereGeometry = new THREE.SphereGeometry(1, 32, 32)
    const sphereMaterial = new THREE.MeshPhongMaterial({
      color: 0x627d98, // primary-500
      transparent: true,
      opacity: 0.15,
      side: THREE.DoubleSide,
    })
    const sphere = new THREE.Mesh(sphereGeometry, sphereMaterial)
    scene.add(sphere)

    // Create wireframe
    const wireframe = new THREE.WireframeGeometry(sphereGeometry)
    const line = new THREE.LineSegments(wireframe)
    const lineMaterial = line.material as THREE.LineBasicMaterial
    lineMaterial.color = new THREE.Color(0x9fb3c8) // primary-300
    lineMaterial.opacity = 0.4
    lineMaterial.transparent = true
    scene.add(line)

    // Create axes (brighter colors for dark background)
    createAxis(new THREE.Vector3(1.3, 0, 0), 0xff6b6b, 'X') // Brighter red
    createAxis(new THREE.Vector3(0, 1.3, 0), 0x90ee90, 'Y') // Brighter green
    createAxis(new THREE.Vector3(0, 0, 1.3), 0x6495ed, 'Z') // Brighter blue

    // Create state vector arrow (initially pointing up |0⟩)
    const direction = new THREE.Vector3(0, 0, 1)
    const origin = new THREE.Vector3(0, 0, 0)
    const length = 1
    const color = 0xff8c42 // Orange-brown for visibility and contrast with RGB axes

    stateVector = new THREE.ArrowHelper(
      direction,
      origin,
      length,
      color,
      0.3,
      0.15,
    )
    scene.add(stateVector)

    // Add pole labels (lighter colors for dark background)
    addLabel('|0⟩', new THREE.Vector3(0, 0, 1.5), 0x6495ed) // Brighter blue
    addLabel('|1⟩', new THREE.Vector3(0, 0, -1.5), 0xff6b6b) // Brighter red
  }

  function createAxis(direction: THREE.Vector3, color: number, label: string) {
    const origin = new THREE.Vector3(0, 0, 0)
    const arrow = new THREE.ArrowHelper(
      direction.clone().normalize(),
      origin,
      direction.length(),
      color,
      0.15,
      0.1,
    )
    scene.add(arrow)

    // Add negative direction
    const negArrow = new THREE.ArrowHelper(
      direction.clone().normalize().negate(),
      origin,
      direction.length(),
      color,
      0.15,
      0.1,
    )
    scene.add(negArrow)
  }

  function addLabel(text: string, position: THREE.Vector3, color: number) {
    const canvas = document.createElement('canvas')
    const context = canvas.getContext('2d')
    if (!context) return

    canvas.width = 128
    canvas.height = 64
    context.font = 'Bold 48px Arial'
    context.fillStyle = `#${color.toString(16).padStart(6, '0')}`
    context.textAlign = 'center'
    context.textBaseline = 'middle'
    context.fillText(text, 64, 32)

    const texture = new THREE.CanvasTexture(canvas)
    const spriteMaterial = new THREE.SpriteMaterial({ map: texture })
    const sprite = new THREE.Sprite(spriteMaterial)
    sprite.position.copy(position)
    sprite.scale.set(0.5, 0.25, 1)
    scene.add(sprite)
  }

  function updateStateVector(vec: BlochVectorResponse) {
    const direction = new THREE.Vector3(vec.x, vec.y, vec.z).normalize()
    const length = Math.sqrt(vec.x * vec.x + vec.y * vec.y + vec.z * vec.z)

    console.log('Updating Bloch vector:', { x: vec.x, y: vec.y, z: vec.z, length })

    stateVector.setDirection(direction)
    stateVector.setLength(length, 0.3, 0.15)
  }

  function animate() {
    animationId = requestAnimationFrame(animate)

    // Update controls for damping
    controls.update()

    renderer.render(scene, camera)
  }
</script>

<div
  class="bloch-sphere rounded-xl border border-primary-600 bg-primary-800 p-6 shadow-lg"
>
  <h2 class="mb-4 text-2xl font-bold text-primary-100">Bloch Sphere</h2>

  <div bind:this={container} class="bloch-container h-96 w-full"></div>

  {#if blochVector}
    <div class="mt-4 rounded-lg bg-primary-700 p-4">
      <h3 class="mb-2 font-semibold text-primary-100">Bloch Vector</h3>
      <div class="font-mono text-sm text-primary-200">
        <div>X: {blochVector.x.toFixed(4)}</div>
        <div>Y: {blochVector.y.toFixed(4)}</div>
        <div>Z: {blochVector.z.toFixed(4)}</div>
        <div class="mt-2">
          Length: {Math.sqrt(
            blochVector.x ** 2 + blochVector.y ** 2 + blochVector.z ** 2,
          ).toFixed(4)}
        </div>
      </div>
    </div>
  {/if}
</div>

<style>
  .bloch-container {
    position: relative;
    overflow: hidden;
  }
</style>
