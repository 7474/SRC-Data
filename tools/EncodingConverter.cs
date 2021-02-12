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
    class EncodingConverter
    {
        internal static async System.Threading.Tasks.Task ExecuteAsync(string[] args)
        {
            var directories = new string[]{
                "GSCデータパック",
                };

            try
            {
                Encoding.RegisterProvider(CodePagesEncodingProvider.Instance);
                var fromEnc = Encoding.GetEncoding(932);
                foreach (var directory in directories)
                {
                    foreach (var file in Directory.EnumerateFiles(
                        directory, "*.txt", SearchOption.AllDirectories))
                    {
                        await ExecuteAsync(file, fromEnc, Encoding.UTF8);
                    }
                    foreach (var file in Directory.EnumerateFiles(
                        directory, "*.eve", SearchOption.AllDirectories))
                    {
                        await ExecuteAsync(file, fromEnc, Encoding.UTF8);
                    }
                }
            }
            catch (Exception e)
            {
                Console.Error.WriteLine(e.Message);
            }
        }

        internal static async System.Threading.Tasks.Task ExecuteAsync(
            string filePath,
            Encoding fromEnc,
            Encoding toEnc
            )
        {
            bool convert = false;
            byte[] converted;
            using (var input = new FileStream(filePath, FileMode.Open))
            using (var inputMs = new MemoryStream())
            {
                await input.CopyToAsync(inputMs);
                var inputBytes = inputMs.ToArray();
                var inputStringFromEnc = fromEnc.GetString(inputBytes);
                var inputStringToEnc = toEnc.GetString(inputBytes);

                converted = toEnc.GetBytes(inputStringFromEnc);
                convert = !inputBytes.SequenceEqual(toEnc.GetBytes(inputStringToEnc));
            }
            if (convert)
            {
                using (var output = new FileStream(filePath, FileMode.Create))
                {
                    await output.WriteAsync(converted);
                    Console.WriteLine($"Converted {filePath}");
                }
            }
            else
            {
                Console.WriteLine($"Skip {filePath}");
            }
        }
    }
}