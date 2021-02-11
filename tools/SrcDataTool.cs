using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Text.Encodings.Web;
using System.Text.Json;
using System.Text.Unicode;
using System.Text;

namespace SrcDataTools
{
        class SrcDataTool
    {
        static void Main(string[] args)
        {
            CreateIndex.Execute(args);
            CreateBitmapIndex.Execute(args);
        }
    }
}