using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Text.Encodings.Web;
using System.Text.Json;
using System.Text.Unicode;

namespace CreateIndex
{
    class TitleData
    {
        public string Title { get; set; }
        public string Base { get; set; }
        public string Path { get; set; }
        public ICollection<string> Tags { get; set; }
    }
    class SrcData
    {
        public ICollection<TitleData> Titles { get; set; }
    }
    class Program
    {
        static void Main(string[] args)
        {
            var directories = new string[]{
                "GSCデータパック/ロボ",
                "GSCデータパック/拡張",
                };

            var titles = new List<TitleData>();
            try
            {
                foreach (var directory in directories)
                {
                    var titleDirectories = Directory.EnumerateDirectories(directory);

                    foreach (string titleDirectory in titleDirectories)
                    {
                        var title = new TitleData
                        {
                            Title = Path.GetFileName(titleDirectory),
                            Base = directory,
                            Path = string.Join("/", directory, Path.GetFileName(titleDirectory)),
                            Tags = directory.Split('/', '\\').ToList(),
                        };
                        titles.Add(title);
                    }
                }
                var data = new SrcData
                {
                    Titles = titles,
                };
                Console.WriteLine(JsonSerializer.Serialize(data, new JsonSerializerOptions()
                {
                    Encoder = JavaScriptEncoder.Create(UnicodeRanges.All),
                    PropertyNamingPolicy = JsonNamingPolicy.CamelCase,
                    WriteIndented = true,
                }));
            }
            catch (Exception e)
            {
                Console.Error.WriteLine(e.Message);
            }
        }
    }
}