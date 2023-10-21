using MyStockmarketBackend.Generators;
using MyStockmarketBackend.Interfaces;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace MyStockmarketBackend.WorldInfo
{
    public class Company
    {
        public string Name { get; set; } = "";
        public string Country { get; set; } = "";
        public string Region { get; set; } = "";
        public string City { get; set; } = "";
        public string Adress { get; set; } = "";
        public int Employees { get; set; }
        public DateTime IPO {  get; set; } = DateTime.Now;
        public Stock Stock { get; set; }
        public bool IsPrivateEquity { get; set; }

        /// <summary>
        /// Initialize a publicly traded company.
        /// </summary>
        /// <param name="dataRetriever">Retriever to get the stock info for this company.</param>
        /// <param name="ticker">Ticker of the stock to retrieve.</param>
        public Company(IDataRetriever dataRetriever, string ticker) 
        {
            if ((ticker is null))
            {
                Stock = StockGenerator.GenerateStock(this, IPO);

            }
            else
            {
                Stock = dataRetriever.LoadStock(ticker);
            }
        }



    }
}
