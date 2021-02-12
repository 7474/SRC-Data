using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Text.Encodings.Web;
using System.Text.Json;
using System.Text.Unicode;
using System.Text;
using System.Threading.Tasks;

namespace SrcDataTools
{
    class SrcDataTool
    {
        static async Task Main(string[] args)
        {
            CreateIndex.Execute(args);
            CreateBitmapIndex.Execute(args);
            await EncodingConverter.ExecuteAsync(args);
        }
    }
}