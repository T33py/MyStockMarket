using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using MyStockmarketBackend.WorldInfo;

namespace MyStockmarketBackend.Interfaces
{
    public interface IDataRetriever
    {
        /// <summary>
        /// Retrieve the general marketdata for the market.
        /// </summary>
        /// <returns>The market object for the session</returns>
        Market LoadMarket();

        /// <summary>
        /// Retrieve the fully instantiated stock dataobject.
        /// </summary>
        /// <param name="ticker">Ticker of the stock</param>
        /// <returns>The full marketinfo of the stock</returns>
        Stock LoadStock(string ticker);

        /// <summary>
        /// Fill in the full information about the stock provided.
        /// </summary>
        /// <param name="stock">Stock to fill info on</param>
        /// <returns>The stock object provided as argument</returns>
        Stock LoadStock(Stock stock);
    }
}
