# Instrucciones de Uso del Agente de Trading

## 📖 Tabla de Contenidos

1. [Inicio Rápido](#inicio-rápido)
2. [Componentes Principales](#componentes-principales)
3. [Cómo Funciona](#cómo-funciona)
4. [Configuración Avanzada](#configuración-avanzada)
5. [Monitoreo y Logs](#monitoreo-y-logs)
6. [Troubleshooting](#troubleshooting)

## Inicio Rápido

### 1. Instalación Rápida

```bash
# Clonar y configurar
git clone https://github.com/cesartavera890-arch/forex-trading-agent.git
cd forex-trading-agent

# Entorno virtual
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt

# Configurar
cp config.example.env .env
# Editar .env con tus credenciales

# Crear directorios
mkdir -p logs database
```

### 2. Ejecutar el Agente

**Opción A: Análisis único**
```bash
python main.py
```

**Opción B: Monitoreo continuo (recomendado)**
```bash
python run_all.py
```

## Componentes Principales

### 1. **Análisis de Noticias** 📰
- Obtiene noticias de EUR/USD cada hora
- Analiza sentimiento (Positivo, Negativo, Neutral)
- Identifica patrones en las noticias

**Archivo:** `analyzers/news_analyzer.py`

### 2. **Análisis Técnico** 📊
- Calcula RSI (Relative Strength Index)
- Calcula MACD (Moving Average Convergence Divergence)
- Calcula Bandas de Bollinger
- Identifica tendencias

**Archivo:** `analyzers/technical_analysis.py`

### 3. **Generador de Señales** ⚡
- Combina análisis de noticias + técnico
- Genera señales BUY/SELL
- Calcula confianza de la señal

**Archivo:** `trading/signals.py`

### 4. **Notificaciones** 📢
- **Email**: Notificaciones automáticas
- **Telegram**: Bot de alertas
- **Discord**: Webhooks para alertas

**Archivos:** `notifications/`

### 5. **Integración OANDA** 🏦
- Obtiene precios en tiempo real
- Coloca órdenes de compra/venta
- Obtiene histórico de velas (candles)

**Archivo:** `trading/oanda_client.py`

## Cómo Funciona

### Flujo General

```
1. Obtener Noticias EUR/USD
   ↓
2. Analizar Sentimiento
   ↓
3. Obtener Datos de OANDA (precios, velas)
   ↓
4. Análisis Técnico (RSI, MACD, Bollinger)
   ↓
5. Generar Señales (BUY/SELL)
   ↓
6. Enviar Notificaciones (Email, Telegram, Discord)
   ↓
7. Guardar en Base de Datos
```

### Criterios de Señal

#### COMPRA (BUY) cuando:
✅ Noticias positivas sobre EUR/USD
✅ RSI < 30 (sobreventa)
✅ MACD bullish (positivo)
✅ Precio bajo bandas Bollinger inferiores
✅ Tendencia alcista

#### VENTA (SELL) cuando:
✅ Noticias negativas sobre EUR/USD
✅ RSI > 70 (sobrecompra)
✅ MACD bearish (negativo)
✅ Precio alto bandas Bollinger superiores
✅ Tendencia bajista

## Configuración Avanzada

### Ajustar Intervalo de Verificación

En `.env`:
```env
CHECK_INTERVAL=3600  # Cambiar a 1800 para 30 minutos
```

### Cambiar Par de Divisas

Modificar en `main.py`:
```python
signals = SignalGenerator.generate_signals('GBP_USD')  # Cambiar EUR_USD
```

### Ajustar Niveles de Riesgo

En `.env`:
```env
MAX_RISK_PERCENTAGE=2      # Máximo 2% de riesgo por operación
STOP_LOSS_PIPS=50          # Stop loss en 50 pips
TAKE_PROFIT_PIPS=100       # Take profit en 100 pips
```

### Cambiar Confianza Mínima

En `trading/signals.py`:
```python
MIN_SIGNAL_STRENGTH=0.6  # 60% mínimo de confianza
```

## Monitoreo y Logs

### Ver Logs en Tiempo Real

```bash
# Ver últimas líneas
tail -f logs/trading.log

# Ver últimas 50 líneas
tail -n 50 logs/trading.log

# Buscar errores
grep "❌" logs/trading.log
```

### Archivos de Log

- **logs/trading.log**: Registro completo de todas las operaciones

### Estructura de Logs

```
2026-06-04 15:30:45 - root - INFO - 🚀 INICIANDO FOREX TRADING AGENT
2026-06-04 15:30:46 - root - INFO - 📦 Inicializando base de datos...
2026-06-04 15:30:47 - root - INFO - 🔐 Verificando credenciales de OANDA...
2026-06-04 15:30:48 - root - INFO - ✅ Conectado a OANDA
2026-06-04 15:30:49 - root - INFO - 📰 Obteniendo noticias EUR/USD...
```

## Base de Datos

### Tablas Disponibles

1. **news_records**: Historial de noticias analizadas
2. **trading_signals**: Señales de trading generadas
3. **trading_records**: Operaciones ejecutadas
4. **alert_logs**: Registro de notificaciones

### Consultar Base de Datos

```python
from database import get_session
from database import NewsRecord, TradingSignal

session = get_session()

# Últimas 10 noticias positivas
positive_news = session.query(NewsRecord).filter_by(sentiment='positive').limit(10).all()

# Últimas 5 señales
recent_signals = session.query(TradingSignal).order_by(TradingSignal.created_at.desc()).limit(5).all()

session.close()
```

## Troubleshooting

### Problema: "ModuleNotFoundError: No module named..."

**Solución:**
```bash
# Activar entorno virtual
source venv/bin/activate  # Windows: venv\Scripts\activate

# Reinstalar dependencias
pip install -r requirements.txt --upgrade
```

### Problema: "Could not connect to OANDA"

**Soluciones:**
- Verifica tu API Key en `.env`
- Verifica tu Account ID
- Verifica que uses `practice` para demo
- Verifica tu conexión a internet

```bash
# Probar conexión
python -c "from trading import OandaClient; print(OandaClient.get_account_info())"
```

### Problema: "No se reciben emails"

**Soluciones:**
1. Habilita "Contraseñas de aplicación" en Google
2. Usa la contraseña de aplicación, no la de tu cuenta
3. Verifica que EMAIL_ENABLED=true
4. Revisa los logs: `grep "email" logs/trading.log`

```env
EMAIL_SENDER=tu_email@gmail.com
EMAIL_PASSWORD=tu_contraseña_de_app  # NO tu contraseña normal
```

### Problema: "Bot de Telegram no responde"

**Soluciones:**
1. Verifica que TELEGRAM_ENABLED=true
2. Verifica el token del bot
3. Asegúrate de haber iniciado conversación con el bot
4. Prueba el bot: `/status`

### Problema: "Señales no se generan"

**Soluciones:**
- Verifica que haya suficientes noticias
- Verifica los logs para ver el análisis
- Aumenta MIN_SIGNAL_STRENGTH si es muy restrictivo
- Verifica que NewsAPI tenga respuesta

```bash
# Debug
python -c "from analyzers import NewsAnalyzer; print(NewsAnalyzer.fetch_eur_usd_news())"
```

### Problema: Base de datos corrupta

**Solución:**
```bash
# Eliminar BD y recrear
rm database/trading.db
python main.py  # Se recreará automáticamente
```

## Consejos Importantes ⚠️

1. **Siempre comienza en PRACTICE**: Usa `OANDA_ENVIRONMENT=practice` primero
2. **Monitorea activamente**: No dejes el agente sin supervisión
3. **Revisa los logs regularmente**: Detecta problemas temprano
4. **Ajusta según experiencia**: Cada mercado es diferente
5. **No uses dinero que no puedas perder**: Trading conlleva riesgos

## Contacto y Soporte

- 📧 Email: cesartavera890@gmail.com
- 🐙 GitHub: [@cesartavera890-arch](https://github.com/cesartavera890-arch)
- 💬 Issues: [Crear issue](https://github.com/cesartavera890-arch/forex-trading-agent/issues)

---

**¡Buena suerte con tus operaciones!** 🚀📈
