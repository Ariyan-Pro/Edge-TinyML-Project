import os

def explore_dataset():
    data_path = "../data/emotion_dataset/Audio_Speech_Actors_01-24"
    
    print("🔍 EXPLORING RAVDESS DATASET STRUCTURE")
    print("=" * 50)
    
    actor_count = 0
    file_count = 0
    
    for actor_dir in os.listdir(data_path):
        actor_path = os.path.join(data_path, actor_dir)
        if os.path.isdir(actor_path):
            actor_count += 1
            files = [f for f in os.listdir(actor_path) if f.endswith('.wav')]
            file_count += len(files)
            
            if actor_count <= 3:  # Show first 3 actors as sample
                print(f"\\n🎭 {actor_dir}: {len(files)} audio files")
                for i, file in enumerate(files[:3]):  # Show first 3 files
                    print(f"   📄 {file}")
    
    print(f"\\n📊 DATASET SUMMARY:")
    print(f"   Total Actors: {actor_count}")
    print(f"   Total Audio Files: {file_count}")
    print(f"   Average files per actor: {file_count/actor_count:.1f}")

if __name__ == "__main__":
    explore_dataset()
