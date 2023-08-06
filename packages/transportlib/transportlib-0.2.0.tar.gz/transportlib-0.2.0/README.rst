Data Pipeline as Transports
-----------------------------------------

This is a library which contains different transports as data pipelines.




Usage
-------------------------------------------------


As Library
~~~~~~~~~~~~~~~

- Available Transport Classes

    - transportlib.transport.yfinance_transport.stock_price.HistoricalStockPriceTransport
    - transportlib.transport.postgres_transport.PostgresTransport



As Image
~~~~~~~~~~~~~~~
.. code-block::
    python ./main {pipeline_name} {watermark_val_prev} {watermark_val_curr}
