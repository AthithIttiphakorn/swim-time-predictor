using System;
using System.IO;
using System.Net.Http;
using System.Text.Json;
using System.Threading.Tasks;
using SwimRankings.Api;


class Program
{
    static async Task Main(string[] args)
    { 
                
        int swimrankingsId = 4046710;

        var httpClient = new HttpClient();
        var api = new SwimmerApi(httpClient);


        Swimmer swimmer = null; // declare outside

        for (int i = 0; i < 2; i++)
        {
            try
            {
                swimmer = await api.GetAsync(swimrankingsId);
                File.WriteAllText($"{swimrankingsId}.json", JsonSerializer.Serialize(swimmer, new JsonSerializerOptions { WriteIndented = true }));
            }


            catch (Exception ex)
            {
                Console.WriteLine($"An error occurred: {ex.Message}");
                return;
            }

            swimrankingsId++;

        }


        Console.WriteLine(JsonSerializer.Serialize(swimmer, new JsonSerializerOptions { WriteIndented = true }));

        File.WriteAllText($"swimmer_4046710.json", JsonSerializer.Serialize(swimmer, new JsonSerializerOptions { WriteIndented = true }));

            }
}
