"""
Strategy Module for Trading Logic
"""
import logging
from datetime import datetime, timedelta
from database import get_session, TradingRecord

logger = logging.getLogger(__name__)


class TradingStrategy:
    """Estrategia de trading automática"""
    
    @staticmethod
    def execute_signal(signal, oanda_client):
        """
        Ejecutar una señal de trading en OANDA
        
        Args:
            signal: Señal de trading generada
            oanda_client: Cliente de OANDA
            
        Returns:
            dict: Información de la orden colocada
        """
        try:
            # Usar 10,000 unidades por defecto
            units = 10000
            
            order_result = oanda_client.place_order(
                instrument=signal['currency_pair'],
                order_type=signal['signal_type'],
                units=units,
                stop_loss_pips=50,
                take_profit_pips=100
            )
            
            if order_result:
                # Guardar en BD
                session = get_session()
                trading_record = TradingRecord(
                    signal_id=signal.get('id'),
                    order_type=signal['signal_type'],
                    currency_pair=signal['currency_pair'],
                    entry_price=order_result['entry_price'],
                    stop_loss=order_result['stop_loss'],
                    take_profit=order_result['take_profit'],
                    status='OPEN',
                    opened_at=datetime.now()
                )
                session.add(trading_record)
                session.commit()
                session.close()
                
                logger.info(f"✅ Orden ejecutada: {signal['signal_type']} {signal['currency_pair']}")
                return order_result
            else:
                logger.error("❌ Error ejecutando la orden")
                return None
        
        except Exception as e:
            logger.error(f"❌ Error in execute_signal: {str(e)}")
            return None
    
    @staticmethod
    def calculate_risk_reward(entry_price, stop_loss, take_profit, order_type='BUY'):
        """
        Calcular ratio riesgo/recompensa
        
        Args:
            entry_price: Precio de entrada
            stop_loss: Precio de stop loss
            take_profit: Precio de take profit
            order_type: Tipo de orden
            
        Returns:
            dict: Información de riesgo/recompensa
        """
        try:
            if order_type == 'BUY':
                risk = entry_price - stop_loss
                reward = take_profit - entry_price
            else:  # SELL
                risk = stop_loss - entry_price
                reward = entry_price - take_profit
            
            ratio = reward / risk if risk > 0 else 0
            
            return {
                'risk': abs(risk),
                'reward': abs(reward),
                'ratio': ratio,
                'risk_pips': abs(risk) / 0.0001,
                'reward_pips': abs(reward) / 0.0001
            }
        
        except Exception as e:
            logger.error(f"❌ Error calculating risk reward: {str(e)}")
            return None
    
    @staticmethod
    def get_position_size(account_balance, risk_percentage, stop_loss_pips):
        """
        Calcular tamaño de posición basado en riesgo
        
        Args:
            account_balance: Balance de la cuenta
            risk_percentage: Porcentaje de riesgo (ej: 2%)
            stop_loss_pips: Stop loss en pips
            
        Returns:
            int: Tamaño de posición en unidades
        """
        try:
            risk_amount = account_balance * (risk_percentage / 100)
            pip_value = 10  # Para EUR/USD con 1 lote (100,000 unidades)
            loss_per_pip = (stop_loss_pips * pip_value) / 100000
            
            position_size = int(risk_amount / loss_per_pip)
            
            return position_size
        
        except Exception as e:
            logger.error(f"❌ Error calculating position size: {str(e)}")
            return 10000
