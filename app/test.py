from pytube import YouTube, Search
from numerize.numerize import numerize

s = Search(input("Enter: "))
print(f"Found {len(s.results)} results")
for i in s.results:
    i: YouTube
    print(f"{i.title} - {i.author} - {numerize(i.views)} views - {i.watch_url}")
