# The `.cooked` Image Suite

**A professional, compressed binary image format and software suite built with Python.**

The `.cooked` format is a custom-designed image container that prioritizes transparency support and storage efficiency. It uses a 13-byte binary header combined with **Zlib Level 9** lossless compression to ensure your images stay high-quality while taking up minimal disk space.

---

## The .cooked Specification

Every `.cooked` file follows a strict binary structure to ensure cross-platform compatibility.

| Component | Size | Type | Description |
| --- | --- | --- | --- |
| **Signature** | 4 Bytes | `char[4]` | The "Magic Number" — always `COOK`. |
| **Width** | 4 Bytes | `uint32` | The image width in pixels (Little-endian). |
| **Height** | 4 Bytes | `uint32` | The image height in pixels (Little-endian). |
| **Mode** | 1 Byte | `uint8` | `0` = RGB (24-bit), `1` = RGBA (32-bit). |
| **Body** | Variable | `binary` | Zlib-compressed pixel data stream. |

---

## How Compression Works (`zlib`)

Unlike a raw "bitmap," which saves every single color value for every pixel, the `.cooked` format uses **DEFLATE** compression via the `zlib` library.

### 1. Encoding (Creator)

When you create an image, the software transforms the raw pixel stream:

* **Pattern Matching:** It finds repeating sequences of colors. For example, if a background has 50 identical gray pixels, it records a "pointer" to that sequence rather than writing the bytes 50 times.
* **Huffman Coding:** It assigns shorter bit-sequences to the most common colors in your image and longer sequences to rare ones, significantly reducing the total bit count.

### 2. Decoding (Viewer)

When you open a `.cooked` file:

* **Decompression:** The software reads the compressed instructions and perfectly reconstructs the original pixel grid in memory.
* **Lossless Quality:** Unlike JPEGs, which "throw away" data to save space, `.cooked` is **lossless**. The image you view is bit-for-bit identical to the PNG you started with.

---

## Setup & Installation

### For Users (macOS App)

1. Download the `CookedSuite.dmg`.
2. Double-click to mount it and drag **CookedSuite.app** to your **Applications** folder.
3. **Security Note:** Because this is an indie project, macOS may block it. To open, **Right-Click** the app and select **Open**, then click **Open** again on the pop-up.


### Requirements for Setup:
1. `Python 3.10+` installed on the system.
2. `uv package manager for python` installed on the system.
### For Developers (Source Code)
1. **Clone the project:**
```bash
git clone git@github.com:Rohan-Shah-312003/Cooked-Image.git
cd Cooked-Image

```


2. **Setup Environment:**
```bash
uv venv .venv
source .venv/bin/activate
uv pip install -r requirements.txt
```

3. **Run:**
```bash
uv run main.py
```



---

## Testing the Model

A sample file, `shrek.png`, is included in the root directory to test transparency handling.

1. Open the **Create** tab and select `shrek.png`.
2. Notice the conversion: Your new `shrek.cooked` file on the **Desktop** will be roughly **10x smaller** than an uncompressed raw version, matching the efficiency of the original PNG.
3. Switch to the **Viewer** tab to view your newly created `.cooked` file!

---

## 🛠 Troubleshooting

* **App Won't Open:** Go to *System Settings > Privacy & Security* and click **Open Anyway** at the bottom of the page.
