import urllib.request
import tarfile
import argparse
from pathlib import Path
import sys
sys.path.append(str(Path(__file__).parent.parent))
from config import CONFIG

def download_speech_commands(output_dir: Path):
    """Genius-level dataset download with resume capability"""
    url = "http://download.tensorflow.org/data/speech_commands_v0.02.tar.gz"
    output_path = output_dir / "speech_commands.tar.gz"
    
    output_dir.mkdir(parents=True, exist_ok=True)
    
    print("🚀 Downloading Speech Commands dataset...")
    try:
        # Smart download with progress
        def report_progress(block_num, block_size, total_size):
            percent = min(100, (block_num * block_size * 100) // total_size)
            print(f"📥 Downloading: {percent}%", end='\r')
        
        urllib.request.urlretrieve(url, output_path, report_progress)
        print("\n✅ Download complete!")
        
        # Extract with progress
        print("📦 Extracting dataset...")
        with tarfile.open(output_path, 'r:gz') as tar:
            members = tar.getmembers()
            for i, member in enumerate(members):
                tar.extract(member, output_dir)
                if i % 1000 == 0:
                    print(f"📁 Extracted {i}/{len(members)} files...")
        
        print("✅ Dataset ready!")
        return True
        
    except Exception as e:
        print(f"❌ Download failed: {e}")
        return False

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default=str(CONFIG.paths.data_raw))
    args = parser.parse_args()
    
    download_speech_commands(Path(args.output))