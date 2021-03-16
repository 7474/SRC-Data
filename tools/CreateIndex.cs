using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Text.Encodings.Web;
using System.Text.Json;
using System.Text.Unicode;

namespace SrcDataTools
{
    class TitleData
    {
        public string Title { get; set; }
        public string Base { get; set; }
        public string Path { get; set; }
        public ICollection<string> Tags { get; set; }
        public ICollection<string> Files { get; set; }
    }
    class DirectoryData
    {
        public string Path { get; set; }
        public ICollection<string> Tags { get; set; }
    }
    class SrcData
    {
        public ICollection<TitleData> Titles { get; set; }
    }
    class CreateIndex
    {
      internal  static void Execute(string[] args)
        {
            var directories = new DirectoryData[]{
               new DirectoryData{ Path = "GSCデータパック/ロボ", Tags = new List<string>{"GSC","ロボ"} },
               new DirectoryData{ Path = "GSCデータパック/拡張", Tags = new List<string>{"GSC","拡張"} },
            };

            var titles = new List<TitleData>();
            try
            {
                foreach (var directory in directories)
                {
                    var titleDirectories = Directory.EnumerateDirectories(directory.Path);

                    foreach (string titleDirectory in titleDirectories)
                    {
                        var title = new TitleData
                        {
                            Title = Path.GetFileName(titleDirectory),
                            Base = directory.Path,
                            Path = string.Join("/", directory, Path.GetFileName(titleDirectory)),
                            Tags = directory.Tags,
                            Files = Directory.EnumerateFiles(titleDirectory, "*.txt", SearchOption.TopDirectoryOnly)
                                .Select(x => Path.GetFileName(x)).ToList(),
                        };
                        titles.Add(title);
                    }
                }
                var data = new SrcData
                {
                    Titles = titles,
                };
                var dataJson = JsonSerializer.Serialize(data, new JsonSerializerOptions()
                {
                    Encoder = JavaScriptEncoder.Create(UnicodeRanges.All),
                    PropertyNamingPolicy = JsonNamingPolicy.CamelCase,
                    //WriteIndented = true,
                });
                //File.WriteAllText("index.json", dataJson, Encoding.UTF8);
                // UTF-8 BOMなし
                File.WriteAllText("index.json", dataJson);
                //Console.WriteLine(dataJson);
            }
            catch (Exception e)
            {
                Console.Error.WriteLine(e.Message);
            }
        }
    }
}