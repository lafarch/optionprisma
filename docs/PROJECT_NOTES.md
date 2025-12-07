# OptionPrisma: Notas Completas del Proyecto 📚

## Índice
1. [Teoría Financiera: Opciones y Pricing](#1-teoria-financiera-opciones-y-pricing)
2. [Monte Carlo Simulation](#2-monte-carlo-simulation)
3. [Black-Scholes Model](#3-black-scholes-model)
4. [Arquitectura del Proyecto](#4-arquitectura-del-proyecto)
5. [Async Programming en Python](#5-async-programming-en-python)
6. [Estructura de Archivos Detallada](#6-estructura-de-archivos-detallada)
7. [Flujo de Datos Completo](#7-flujo-de-datos-completo)

---

## 1. Teoría Financiera: Opciones y Pricing

### ¿Qué es una Opción?

Una **opción** es un contrato financiero que te da el **derecho** (no la obligación) de comprar o vender un activo a un precio específico antes de una fecha determinada.

#### Tipos de Opciones:

**CALL Option (Opción de Compra)**
```
Derecho a COMPRAR el activo al precio K (strike)
Payoff al vencimiento: max(S_T - K, 0)

Ejemplo:
- Compras una Call de Apple con K=$100
- Si Apple vale $120 al vencimiento → Ganas $20
- Si Apple vale $80 al vencimiento → No ejerces (pierdes solo la prima)
```

**PUT Option (Opción de Venta)**
```
Derecho a VENDER el activo al precio K (strike)
Payoff al vencimiento: max(K - S_T, 0)

Ejemplo:
- Compras una Put de Apple con K=$100
- Si Apple vale $80 al vencimiento → Ganas $20
- Si Apple vale $120 al vencimiento → No ejerces
```

### Parámetros Clave:

| Parámetro | Símbolo | Significado |
|-----------|---------|-------------|
| Spot Price | S₀ | Precio actual del activo |
| Strike Price | K | Precio de ejercicio |
| Time to Maturity | T | Tiempo hasta vencimiento (años) |
| Volatility | σ | Volatilidad anual (desviación estándar) |
| Risk-free Rate | r | Tasa libre de riesgo |

### ¿Por qué es difícil valorar opciones?

El precio de una opción NO es simplemente `S₀ - K` porque:
1. **Incertidumbre**: El precio futuro del activo es desconocido
2. **Tiempo**: El valor del dinero cambia con el tiempo
3. **Volatilidad**: Mayor incertidumbre = mayor valor de la opción
4. **Asimetría**: Ganancias ilimitadas, pérdidas limitadas

---

## 2. Monte Carlo Simulation

### Concepto Fundamental

**Monte Carlo** es un método que usa simulaciones aleatorias para resolver problemas complejos.

### Idea:

1. Simular muchos posibles futuros del precio de la acción
2. Calcular el payoff en cada escenario
3. Promediar todos los payoffs
4. Descontar al valor presente

### Matemática Detallada

**Geometric Brownian Motion (GBM)**

Las acciones se modelan como un proceso estocástico:

```math
dS = mu S dt + sigma S dW
```

### Por qué el término (r - 0.5 sigma^2)

Esto es el *drift ajustado por riesgo*:
- `mu` es el rendimiento esperado (drift)
- `sigma` es la volatilidad

---

# 3. Black-Scholes Model
### Historia

Desarrollado por Fischer Black, Myron Scholes y Robert Merton (1973). Revolucionó las finanzas y ganó el Premio Nobel en 1997.

### Fórmula Analítica

- CALL y PUT prices

---

# 4. Arquitectura del Proyecto

### Partes del Proyecto

- Entradas de usuario
- Simulaciones
- Black-Scholes (analytical)
- Async Programming in Python
- Estructura de Archivos
- Flujo de Datos: ingestion → compute → store

---

# 5. Async Programming 

### Cosas a saber

- Non-blocking I/O operations
- Concurrent request handling
- Async file operations with `aiofiles`

---

# 6. Matematica Detallada

### Geometric Brownian Motion (GBM)

Las acciones se modelan como un proceso estocástico:

```math
dS = mu S dt + sigma S dW
```

---

# 7. Flujo de Datos Completo

- Spot Price
- Strike Price
- Time to Maturity
- Volatility
- Risk-free rate
- Option type

---

# 8. Desarrollo y Productividad

- Use `fastapi dev` para el mejor developer experience:
    - Auto-reload on code changes
    - Better error messages
    - Automatic configuration

---

# 9. Testing

- Run all tests: `pytest -v`

---

# 10. Contribuciones

- Create an issue or submit a Pull Request.

---

# Apéndice: Recursos Claves

- Black-Scholes-Merton model for option pricing
- FastAPI documentation
- Quantitative finance references
- **BS**: Para validar que MC funciona correctamente

### The Greeks (Las Griegas)

Las **Greeks** miden sensibilidad del precio de la opción a cambios en parámetros:

#### 1. Delta (Δ)
```
Δ = ∂C/∂S

Significado: Cambio en precio de opción por $1 de cambio en el activo
Rango: [0, 1] para calls, [-1, 0] para puts

Ejemplo:
Delta = 0.6 significa:
"Si la acción sube $1, la opción sube $0.60"
```

#### 2. Gamma (Γ)
```
Γ = ∂²C/∂S² = ∂Δ/∂S

Significado: Tasa de cambio de Delta
"Curvatura" del precio de la opción

Importante para: Hedging dinámico
```

#### 3. Vega (ν)
```
ν = ∂C/∂σ

Significado: Cambio en precio por 1% de cambio en volatilidad

Ejemplo:
Vega = 0.30 significa:
"Si la volatilidad sube de 20% a 21%, la opción sube $0.30"
```

#### 4. Theta (Θ)
```
Θ = ∂C/∂t

Significado: "Time decay" - pérdida de valor por paso del tiempo
Usualmente negativo (opciones pierden valor con el tiempo)

Ejemplo:
Theta = -0.05 significa:
"La opción pierde $0.05 por día"
```

#### 5. Rho (ρ)
```
ρ = ∂C/∂r

Significado: Sensibilidad a tasas de interés
Menos importante en la práctica (tasas cambian poco)
```

### Implementación en el Código

**Archivo: `app/black_scholes.py`**

```python
def black_scholes_price(...):
    # Calcular d1 y d2
    d1 = (np.log(spot_price / strike_price) 
          + (risk_free_rate + 0.5 * volatility**2) * time_to_maturity) \
         / (volatility * np.sqrt(time_to_maturity))
    
    d2 = d1 - volatility * np.sqrt(time_to_maturity)
    
    # Para CALL
    if option_type == "call":
        price = (spot_price * norm.cdf(d1) 
                - strike_price * np.exp(-risk_free_rate * time_to_maturity) 
                * norm.cdf(d2))
```

**¿Qué es `norm.cdf()`?**
- CDF = Cumulative Distribution Function
- `norm.cdf(x)` = P(Z ≤ x) donde Z ~ N(0,1)
- Nos da la probabilidad acumulada bajo la curva normal

---

## 4. Arquitectura del Proyecto 

### Patrón de Diseño: Separation of Concerns

```
┌─────────────────────────────────────────────┐
│            API Layer (main.py)              │
│  - Maneja HTTP requests/responses           │
│  - Validación de entrada (Pydantic)         │
│  - Orquestación de operaciones              │
└─────────────┬───────────────────────────────┘
              │
              ├──► Business Logic Layer
              │    ├── monte_carlo.py (Simulación)
              │    └── black_scholes.py (Fórmulas)
              │
              └──► Persistence Layer
                   └── persistence.py (CRUD JSON)
```

### ¿Por qué esta estructura?

**1. Testabilidad:**
```python
# Puedes testear la lógica sin necesidad de FastAPI
def test_monte_carlo():
    result = price_european_option(...)
    assert result["price"] > 0
```

**2. Reutilización:**
```python
# El mismo código puede usarse en:
# - API REST
# - Script de línea de comandos
# - Jupyter Notebook
# - Otra API
```

**3. Mantenibilidad:**
```
Cambiar de JSON a PostgreSQL:
✅ Solo modificas persistence.py
❌ No tocas monte_carlo.py ni black_scholes.py
```

---

## 5. Async Programming en Python

### El Problema del Blocking

**Código Síncrono (Blocking):**
```python
def get_data():
    time.sleep(2)  # Esperando respuesta de API
    return data

# Si 10 usuarios llaman esto:
# Usuario 1: 0-2s
# Usuario 2: 2-4s (esperando al 1)
# Usuario 3: 4-6s (esperando al 2)
# ...
# Usuario 10: 18-20s ❌
```

**Código Asíncrono (Non-blocking):**
```python
async def get_data():
    await asyncio.sleep(2)  # Cede control al event loop
    return data

# Si 10 usuarios llaman esto:
# Usuarios 1-10: 0-2s (todos en paralelo) ✅
```

### Event Loop

```
┌─────────────────────────────────────────────┐
│           Event Loop (Uvicorn)              │
│                                             │
│  ┌─────────┐  ┌─────────┐  ┌─────────┐    │
│  │ Request │  │ Request │  │ Request │    │
│  │    1    │  │    2    │  │    3    │    │
│  └────┬────┘  └────┬────┘  └────┬────┘    │
│       │            │            │          │
│       ▼            ▼            ▼          │
│  await I/O    await I/O    await I/O      │
│       │            │            │          │
│       └────────────┴────────────┘          │
│              (paralelo)                    │
└─────────────────────────────────────────────┘
```

### Cuándo usar `async` vs `def`

**Use `async def` para:**
- ✅ I/O operations (leer/escribir archivos, red, DB)
- ✅ Operaciones que "esperan"
- ✅ Consistencia en endpoints FastAPI

**Use `def` para:**
- ✅ CPU-bound operations (matemáticas intensivas)
- ✅ Funciones puras sin I/O

**Ejemplo en nuestro proyecto:**

```python
# ❌ INCORRECTO - No hacer async en CPU-bound
async def price_european_option(...):
    # Monte Carlo es CPU-intensive, no se beneficia de async
    pass

# ✅ CORRECTO
def price_european_option(...):
    # Computación pura, dejar sync
    pass

# ✅ CORRECTO - El endpoint SÍ es async
async def create_simulation(request):
    await validate_inputs_async(request)  # I/O
    result = price_european_option(...)    # CPU (sync dentro de async)
    await save_simulation_result(result)   # I/O
```

### `await` keyword

```python
# Esto PAUSA la función y devuelve control al event loop
result = await some_async_function()

# Es como decir:
# "Mientras espero esto, puedes hacer otras cosas"
```

**Regla de oro:**
```
async def   → Puede usar await
def         → NO puede usar await
await       → Solo dentro de async def
```

---

## 6. Estructura de Archivos Detallada 

### `app/config.py`
```python
"""
Configuración centralizada del proyecto
"""
# Rutas de archivos
BASE_DIR = Path(__file__).resolve().parent.parent
RESULTS_FILE = DATA_DIR / "results.json"

# Constantes de la aplicación
APP_NAME = "OptionPrisma"
DEFAULT_SIMULATIONS = 100_000
```

**¿Por qué un archivo de config?**
- ✅ Single source of truth
- ✅ Fácil cambiar paths en desarrollo vs producción
- ✅ No hardcodear valores en el código

---

### `app/models.py`
```python
"""
Modelos Pydantic para validación
"""
class OptionPricingRequest(BaseModel):
    spot_price: float = Field(..., gt=0)
    # ...
```

**¿Qué hace Pydantic?**

1. **Validación automática:**
```json
// Request
{"spot_price": -100}

// Pydantic rechaza automáticamente
{
  "detail": [
    {
      "loc": ["spot_price"],
      "msg": "ensure this value is greater than 0"
    }
  ]
}
```

2. **Type coercion:**
```json
// Request
{"spot_price": "100"}  // String

// Pydantic convierte automáticamente
spot_price = 100.0  // Float
```

3. **Documentación automática:**
FastAPI usa los modelos Pydantic para generar el Swagger UI.

---

### `app/monte_carlo.py`

**Función principal:**
```python
def price_european_option(...) -> dict[str, float]:
```

**Returns:**
```python
{
    "price": 10.45,          # Precio de la opción
    "std_error": 0.03,       # Error estándar
    "confidence_interval_95": 0.06  # 95% CI
}
```

**Función auxiliar:**
```python
def validate_pricing_inputs(...) -> tuple[bool, str]:
```

**Returns:**
```python
(True, "")  # Si es válido
(False, "Volatility cannot be negative")  # Si no es válido
```

---

### `app/black_scholes.py`

**Dos funciones principales:**

1. **Pricing:**
```python
def black_scholes_price(...) -> float:
    # Devuelve el precio exacto según fórmula BS
```

2. **Greeks:**
```python
def calculate_greeks(...) -> dict[str, float]:
    return {
        "delta": 0.5432,
        "gamma": 0.0234,
        "vega": 0.3456,
        "theta": -0.0123,
        "rho": 0.2345
    }
```

---

### `app/persistence.py`

**CRUD Operations:**

```python
async def save_simulation_result(result: SimulationResult) -> None:
    # CREATE: Guardar nuevo resultado
    
async def get_simulation_result(id: str) -> Optional[SimulationResult]:
    # READ: Obtener resultado específico
    
async def get_all_simulation_results() -> List[SimulationResult]:
    # READ: Obtener todos los resultados
    
async def delete_simulation_result(id: str) -> bool:
    # DELETE: Eliminar resultado
```

**¿Por qué todo es async?**
- Operaciones de archivos son I/O-bound
- `aiofiles` permite lectura/escritura no-bloqueante

---

### `app/main.py` - El Corazón de la API

**Estructura:**

```python
# 1. Imports
from fastapi import FastAPI, HTTPException
# ...

# 2. Inicialización
app = FastAPI(title="OptionPrisma", ...)

# 3. Helper functions
async def fetch_risk_free_rate_async():
    # Simula llamada a API externa
    
async def validate_inputs_async():
    # Validación asíncrona

# 4. Endpoints
@app.get("/")                    # Health check
@app.post("/simulations")        # CREATE
@app.get("/simulations/{id}")    # READ (uno)
@app.get("/simulations")         # READ (todos)
@app.delete("/simulations/{id}") # DELETE
```

---

## 7. Flujo de Datos Completo 

### Ejemplo: Crear una simulación

**1. Cliente hace request:**
```bash
POST /simulations
{
  "spot_price": 100,
  "strike_price": 105,
  "time_to_maturity": 1.0,
  "volatility": 0.25,
  "risk_free_rate": 0.05,
  "option_type": "call"
}
```

**2. FastAPI recibe el request:**
```python
@app.post("/simulations")
async def create_simulation(request: OptionPricingRequest):
    # Pydantic valida automáticamente el JSON
```

**3. Validación asíncrona:**
```python
await validate_inputs_async(request)
# Simula check de DB: ¿El ticker existe?
# Simula check de Redis: ¿El usuario tiene quota?
```

**4. Simulación de fetch externo:**
```python
await fetch_risk_free_rate_async()
# Simula llamada a FRED API para obtener tasa actual
# En este proyecto, solo simulamos el delay
```

**5. Cálculo Monte Carlo (CPU-bound, sync):**
```python
pricing_result = price_european_option(
    spot_price=100,
    strike_price=105,
    # ...
)
# Devuelve: {"price": 10.45, "std_error": 0.03, ...}
```

**6. Cálculo Black-Scholes (sync):**
```python
bs_price = black_scholes_price(...)
# Devuelve: 10.48

greeks = calculate_greeks(...)
# Devuelve: {"delta": 0.54, "gamma": 0.02, ...}
```

**7. Generar ID único:**
```python
simulation_id = f"sim_{int(time.time())}_{secrets.token_hex(4)}"
# Ejemplo: "sim_1702847562_a3f4c8b2"
```

**8. Guardar en JSON (async I/O):**
```python
result = SimulationResult(
    simulation_id=simulation_id,
    option_price=10.45,
    # ...
)
await save_simulation_result(result)
```

**9. Devolver respuesta:**
```python
return OptionPricingResponse(
    simulation_id="sim_1702847562_a3f4c8b2",
    option_price=10.45,
    std_error=0.03,
    black_scholes_price=10.48,
    greeks={...},
    # ...
)
```

**10. Cliente recibe:**
```json
{
  "simulation_id": "sim_1702847562_a3f4c8b2",
  "option_price": 10.45,
  "std_error": 0.03,
  "confidence_interval_95": 0.06,
  "black_scholes_price": 10.48,
  "greeks": {
    "delta": 0.5432,
    "gamma": 0.0234,
    "vega": 0.3456,
    "theta": -0.0123,
    "rho": 0.2345
  },
  "inputs": { ... },
  "timestamp": "2024-12-17T15:30:45.123Z"
}
```

---

## 📊 Diagrama de Arquitectura Completo

```
┌─────────────────────────────────────────────────────────┐
│                      CLIENT                             │
│  (Browser / cURL / Python requests / Postman)           │
└─────────────────┬───────────────────────────────────────┘
                  │ HTTP Request (JSON)
                  ▼
┌─────────────────────────────────────────────────────────┐
│                 FASTAPI APP (main.py)                   │
│                                                         │
│  ┌─────────────────────────────────────────────────┐   │
│  │  Endpoint: POST /simulations                    │   │
│  │  async def create_simulation(...)               │   │
│  └────────┬────────────────────────────────────────┘   │
│           │                                            │
│           ├──► 1. Pydantic Validation (models.py)     │
│           │      OptionPricingRequest                 │
│           │                                            │
│           ├──► 2. await validate_inputs_async()       │
│           │      (Async I/O simulation)               │
│           │                                            │
│           ├──► 3. await fetch_risk_free_rate_async()  │
│           │      (Async API call simulation)          │
│           │                                            │
│           ├──► 4. price_european_option()             │
│           │      ├── Generate Z ~ N(0,1)              │
│           │      ├── Calculate terminal prices (GBM)  │
│           │      ├── Calculate payoffs                │
│           │      └── Return {"price": ..., "se": ...} │
│           │      (CPU-bound, synchronous)             │
│           │                                            │
│           ├──► 5. black_scholes_price()               │
│           │      └── Analytical solution              │
│           │                                            │
│           ├──► 6. calculate_greeks()                  │
│           │      └── Delta, Gamma, Vega, Theta, Rho   │
│           │                                            │
│           ├──► 7. Generate unique ID                  │
│           │                                            │
│           ├──► 8. await save_simulation_result()      │
│           │      ├── await _read_results_file()       │
│           │      ├── Append new result                │
│           │      └── await _write_results_file()      │
│           │      (Async file I/O)                     │
│           │                                            │
│           └──► 9. Return OptionPricingResponse        │
│                    (Pydantic model → JSON)            │
└─────────────────┬───────────────────────────────────────┘
                  │ HTTP Response (JSON)
                  ▼
┌─────────────────────────────────────────────────────────┐
│                      CLIENT                             │
│  Receives: simulation_id, prices, greeks, etc.         │
└─────────────────────────────────────────────────────────┘
```

---

## 🎯 Conceptos Clave para Recordar

### 1. Risk-Neutral Pricing
```
En el mundo real: μ (rendimiento esperado) varía
En pricing de opciones: usamos r (risk-free rate)

¿Por qué? Teoría de No-Arbitraje:
"El precio de la opción debe ser independiente del rendimiento esperado"
```

### 2. Law of Large Numbers
```
Más simulaciones → Menor error estándar

SE = σ / √N

N = 10,000  → SE alto
N = 100,000 → SE medio
N = 1,000,000 → SE bajo (pero más lento)
```

### 3. Put-Call Parity
```
Relación fundamental:
C - P = S₀ - K*e^(-rT)

Usamos esto para validar nuestros cálculos
```

### 4. Async ≠ Parallel
```
Async: Un solo thread manejando múltiples tareas (I/O)
Parallel: Múltiples threads/procesos (CPU)

Para CPU-intensive (Monte Carlo):
→ multiprocessing, no async
```

---

## 📖 Para Estudiar Más

### Finanzas:
1. **Options, Futures, and Other Derivatives** - John Hull
2. **The Concepts and Practice of Mathematical Finance** - Mark Joshi
3. **Paul Wilmott on Quantitative Finance** - Paul Wilmott

### Python Async:
1. **Real Python: Async IO in Python** - https://realpython.com/async-io-python/
2. **FastAPI Documentation** - https://fastapi.tiangolo.com
3. **Python asyncio docs** - https://docs.python.org/3/library/asyncio.html

### Numerical Methods:
1. **Monte Carlo Methods in Financial Engineering** - Paul Glasserman
2. **Python for Finance** - Yves Hilpisch

---

## ✅ Checklist de Comprensión

Deberías poder responder:

**Finanzas:**
- [ ] ¿Cuál es el payoff de una call vs put?
- [ ] ¿Por qué mayor volatilidad → mayor precio de opción?
- [ ] ¿Qué mide Delta y por qué es importante?
- [ ] ¿Qué es risk-neutral pricing?

**Programación:**
- [ ] ¿Cuándo usar `async def` vs `def`?
- [ ] ¿Por qué usamos NumPy para Monte Carlo?
- [ ] ¿Qué hace Pydantic en nuestro proyecto?
- [ ] ¿Por qué separamos monte_carlo.py de main.py?

**Implementación:**
- [ ] ¿Cómo generamos precios terminales con GBM?
- [ ] ¿Qué es el standard error y por qué importa?
- [ ] ¿Cómo funcionan las operaciones CRUD en JSON?
- [ ] ¿Cuál es el flujo completo de un request?

---

**¡Estas notas te acompañarán en todo el proyecto!** 📚✨