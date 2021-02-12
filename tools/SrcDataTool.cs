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