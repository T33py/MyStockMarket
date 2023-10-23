using MyStockmarketBackend.WorldInfo;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace MyStockmarketBackend.Generators
{
    public static class StockGenerator
    {
        public static Stock GenerateStock(Company company, DateTime ipo)
        {
            Stock stock = new Stock()
            {
                Name = company.Name,
                Company = company,
            };
            return stock;
        }
    }
}
