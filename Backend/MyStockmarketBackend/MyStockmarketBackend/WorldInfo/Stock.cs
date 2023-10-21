using MyStockmarketBackend.TimeSeries;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace MyStockmarketBackend.WorldInfo
{
    public class Stock
    {
        public string Name { get; set; }
        public string Ticker { get; set; }
        public string Description { get; set; }
        public Company Company { get; set; }
        public PriceSeries PriceHistory { get; set; }
        public Keyvalues HistoricKeyvalues { get; set;}

        /// <summary>
        /// TODO: implement if memory becomes an issue.
        /// </summary>
        public void DisposeOfDeepInfo()
        {
            // TODO: 
            //   Remove the deep pricehistory and historic key values to optimize memory footprint?
        }
    }
}