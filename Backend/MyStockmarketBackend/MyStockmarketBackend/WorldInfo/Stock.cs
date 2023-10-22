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
        public PriceSeries PriceInfo { get; set; }
        public List<Keyvalues> HistoricKeyvalues { get; set; } = new List<Keyvalues>();
        public Keyvalues? LatestKeyvalues { get => HistoricKeyvalues.MaxBy(x => x.Year); }

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