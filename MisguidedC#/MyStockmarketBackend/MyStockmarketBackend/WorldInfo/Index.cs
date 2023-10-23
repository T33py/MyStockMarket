using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace MyStockmarketBackend.WorldInfo
{
    public class Index
    {
        public string Name { get; set; } = string.Empty;
        public string Description { get; set; } = string.Empty;
        public List<Company> Companys { get; set; } = new List<Company>();
        public Company LargestCompanyByRevenue { get; set; }
        public Company LargestCompanyByMarketCap { get; set; }
        public Company SmallestCompanyByRevenue { get; set; }
        public Company SmallestCompanyByMarketCap { get; set; }
    }
}
