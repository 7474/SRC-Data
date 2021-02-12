using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Text.Encodings.Web;
using System.Text.Json;
using System.Text.Unicode;

namespace SrcDataTools
{
    class BitmapFolder
    {
        public string Name { get; set; }
        public string Base { get; set; }
        public string Path { get; set; }
        public ICollection<string> Tags { get; set; }
        public ICollection<string> Files { get; set; }
    }
    class SrcBitmapData
    {
        public ICollection<BitmapFolder> Folders { get; set; }
    }
    class CreateBitmapIndex
    {
        internal static void Execute(string[] args)
        {
            var directories = new string[]{
                "Sharp/Bitmap",
                };

            var folders = new List<BitmapFolder>();
            try
            {
                foreach (var directory in directories)
                {
                    var bitmapDirectories = Directory.EnumerateDirectories(directory);

                    foreach (string bitmapDirectory in bitmapDirectories)
                    {
                        var title = new BitmapFolder
                        {
                            Name = Path.GetFileName(bitmapDirectory),
                            Base = directory,
                            Path = string.Join("/", directory, Path.GetFileName(bitmapDirectory)),
                            Tags = directory.Split('/', '\\').Append(Path.GetFileName(bitmapDirectory)).ToList(),
                            Files = Directory.EnumerateFiles(bitmapDirectory, "*.png", SearchOption.TopDirectoryOnly)
                                .Select(x => Path.GetFileName(x)).ToList(),
                        };
                        folders.Add(title);
                    }
                }
                var data = new SrcBitmapData
                {
                    Folders = folders,
                };
                var dataJson = JsonSerializer.Serialize(data, new JsonSerializerOptions()
                {
                    Encoder = JavaScriptEncoder.Create(UnicodeRanges.All),
                    PropertyNamingPolicy = JsonNamingPolicy.CamelCase,
                    //WriteIndented = true,
                });
                //File.WriteAllText("index.json", dataJson, Encoding.UTF8);
                // UTF-8 BOMなし
                File.WriteAllText("index-bitmap.json", dataJson);
                //Console.WriteLine(dataJson);
            }
            catch (Exception e)
            {
                Console.Error.WriteLine(e.Message);
            }
        }
    }
}