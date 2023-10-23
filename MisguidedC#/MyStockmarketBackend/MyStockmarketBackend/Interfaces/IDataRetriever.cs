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
    }
}
