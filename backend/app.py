from recommend import recommend

if __name__ == "__main__":
    print("🎬 Welcome to the Movie Recommendation System!")
    while True:
        movie_name = input("\nEnter a movie name (or type 'exit' to quit): ")
        if movie_name.lower() == 'exit':
            print("👋 Goodbye!")
            break

        result = recommend(movie_name)
        if result[0] == "Movie not found!":
            print("❌ Movie not found! Try again.")
        else:
            print(f"\n💡 Top 5 movies similar to '{movie_name}':")
            for idx, title in enumerate(result, 1):
                print(f"{idx}. {title}")
