from jesse.strategies import Strategy, cached
import jesse.indicators as ta
from jesse import utils

class GoldenCross(Strategy):
    """
    Golden Cross Strategy
    Long when SMA 50 > SMA 200
    Short when SMA 50 < SMA 200
    Filtered by ADX > 25 to avoid ranging markets
    """
    @property
    def fast_sma(self):
        return ta.sma(self.candles, 50)

    @property
    def slow_sma(self):
        return ta.sma(self.candles, 200)

    @property
    def adx(self):
        return ta.adx(self.candles, 14)

    def should_long(self) -> bool:
        return self.fast_sma > self.slow_sma and self.adx > 25

    def should_short(self) -> bool:
        return self.fast_sma < self.slow_sma and self.adx > 25

    def should_cancel_entry(self) -> bool:
        return True

    @property
    def atr(self):
        return ta.atr(self.candles, 14)

    def go_long(self):
        entry_price = self.price
        qty = utils.size_to_qty(self.capital, entry_price)
        self.buy = qty, entry_price
        
        self.stop_loss = qty, entry_price - (self.atr * 2)
        self.take_profit = qty, entry_price + (self.atr * 4)

    def go_short(self):
        entry_price = self.price
        qty = utils.size_to_qty(self.capital, entry_price)
        self.sell = qty, entry_price
        
        self.stop_loss = qty, entry_price + (self.atr * 2)
        self.take_profit = qty, entry_price - (self.atr * 4)

    def update_position(self):
        if self.is_long and self.fast_sma < self.slow_sma:
            self.liquidate()
        
        if self.is_short and self.fast_sma > self.slow_sma:
            self.liquidate()
