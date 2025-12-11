# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Qiskit Viz is a web application for creating interactive visualizations of quantum states from Qiskit. It uses a modern web stack with Svelte/SvelteKit for the frontend and Python/FastAPI for the backend.

## Architecture

### Frontend (frontend/)
- **Framework**: SvelteKit with Svelte 5
- **Styling**: Tailwind CSS v4
- **3D Rendering**: Three.js for quantum state visualizations (Bloch sphere)
- **Data Visualization**: D3.js for statevector probability charts
- **Testing**: Vitest with browser mode (Playwright)
- **Component Development**: Storybook with accessibility testing
- **API Client**: Auto-generated from OpenAPI spec using `@hey-api/openapi-ts`

### Backend (backend/)
- **Framework**: FastAPI
- **Quantum Library**: Qiskit 2.x
- **Package Manager**: uv for fast dependency management
- **Python Version**: >=3.13
- **API**: RESTful endpoints for circuit building, statevector calculation, and Bloch sphere data

### Key Components

#### Frontend Components (`frontend/src/lib/components/`)
1. **CircuitBuilder.svelte** - Interactive UI for building quantum circuits
   - Gate selection (H, X, Y, Z, S, T, Sdg, Tdg, RX, RY, RZ)
   - Parameter input for rotation gates
   - Visual circuit operation list

2. **BlochSphere.svelte** - 3D visualization of single-qubit states
   - Uses Three.js for rendering
   - Shows Bloch vector with X, Y, Z coordinates
   - Animated rotation for better visualization
   - Displays state labels (|0⟩, |1⟩)

3. **StatevectorDisplay.svelte** - Probability distribution visualization
   - D3.js bar chart of basis state probabilities
   - Detailed amplitude table (real, imaginary components)
   - Support for multi-qubit systems

#### Backend API Endpoints (`backend/main.py`)
- `POST /circuit/build` - Build circuit and return QASM
- `POST /circuit/statevector` - Execute circuit and return statevector
- `POST /bloch/{qubit}` - Get Bloch sphere coordinates for specific qubit

### API Integration
The frontend uses auto-generated TypeScript clients from the FastAPI OpenAPI spec. To regenerate:
```bash
cd frontend
npx @hey-api/openapi-ts -i http://localhost:8000/openapi.json -o src/lib/api -c @hey-api/client-fetch
```

## Docker Development Environment

### Container Structure
- **Backend**: Runs as `dev` user in `/home/dev/src`
- **Frontend**: Runs as `node` user in `/home/node/src`
- **User ID**: Configurable via `USERID` env var (default: 1001)
- **Volumes**: Source code mounted with isolated `node_modules` and `.venv`

### Makefile Commands
```bash
make          # Show help
make build    # Build Docker images
make up       # Start services
make down     # Stop services
make logs     # View all logs
make shell-backend   # Shell into backend container
make shell-frontend  # Shell into frontend container
make rebuild  # Full rebuild
```

### Manual Docker Compose
```bash
# Set user ID (optional)
export USERID=$(id -u)

# Start services
docker compose up -d

# View logs
docker compose logs -f

# Stop services
docker compose down
```

## Local Development (without Docker)

### Frontend Development
```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev

# Run type checking
npm run check

# Run linter
npm run lint

# Format code
npm run format

# Run all tests
npm run test

# Run tests in watch mode
npm run test:unit

# Build for production
npm run build

# Start Storybook
npm run storybook
```

### Backend Development
```bash
cd backend

# Install dependencies with uv
uv sync

# Activate virtual environment
source .venv/bin/activate

# Run development server with hot reload
uvicorn main:app --reload

# Or run directly
python main.py
```

## Testing Structure

The frontend uses a dual-test-project setup in Vitest:

1. **Client tests** (`*.svelte.{test,spec}.{js,ts}`): Run in browser mode with Playwright for Svelte component testing
2. **Server tests** (`*.{test,spec}.{js,ts}` excluding Svelte files): Run in Node environment for server-side logic

Tests require assertions (configured with `requireAssertions: true`).

## Project Structure

```
qiskit-viz/
├── frontend/
│   ├── src/
│   │   ├── lib/
│   │   │   ├── api/          # Auto-generated API client
│   │   │   └── components/   # Svelte components
│   │   ├── routes/           # SvelteKit routes
│   │   └── stories/          # Storybook stories
│   ├── Dockerfile
│   └── package.json
├── backend/
│   ├── main.py               # FastAPI application
│   ├── Dockerfile
│   └── pyproject.toml
├── docker-compose.yml
├── Makefile
└── CLAUDE.md
```

## Technology Stack Details

- **Svelte 5**: Uses latest runes API for reactivity (`$state`, `$effect`, `$props`)
- **Tailwind CSS v4**: Using Vite plugin (`@tailwindcss/vite`)
- **TypeScript**: Strict type checking enabled
- **ESLint**: Flat config format with Svelte and TypeScript support
- **Prettier**: Code formatting with Svelte and Tailwind plugins
- **Three.js**: 3D rendering for Bloch sphere visualization
- **D3.js**: Data visualization for probability distributions
- **Qiskit**: IBM's quantum computing SDK for circuit simulation

## Development Workflow

1. **Start the environment**: `make up` or `docker compose up`
2. **Access the application**:
   - Frontend: http://localhost:5173
   - Backend API: http://localhost:8000
   - API Docs: http://localhost:8000/docs
3. **Build a circuit**: Use the Circuit Builder UI to add gates
4. **Execute**: Click "Execute Circuit" to run quantum simulation
5. **Visualize**: View results in Bloch Sphere and Statevector displays

## Common Patterns

### Adding New Gates
1. Update `availableGates` or `parametricGates` in `CircuitBuilder.svelte`
2. Add gate logic in backend `build_circuit()`, `get_statevector()`, and `get_bloch_vector()` functions
3. The API client types will auto-update when regenerated

### Adding New Visualizations
1. Create new Svelte component in `frontend/src/lib/components/`
2. Add Three.js or D3.js visualization logic
3. Import and use in `frontend/src/routes/+page.svelte`
4. Create corresponding backend endpoint if needed

## Notes for AI Assistants

- When modifying Dockerfiles, remember to update both the WORKDIR and COPY paths to match `/home/{user}/src`
- The `node_modules` and `.venv` directories are isolated in Docker volumes to prevent host/container conflicts
- API types are auto-generated; prefer regenerating over manual edits
- Svelte 5 uses runes (`$state`, `$effect`) instead of stores for reactivity
- Backend uses `uv` for dependency management, not pip directly
