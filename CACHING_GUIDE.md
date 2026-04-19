# Smart Cache Invalidation Guide

## Overview

The batch processing endpoint now includes **intelligent caching** that automatically invalidates when file contents change. This speeds up repeated uploads while ensuring you always get results from the latest data.

---

## How It Works

### Cache Key Generation

The cache key is generated from:
1. **Filename** - name of the uploaded file
2. **File size** - total bytes in the file
3. **File contents** - SHA256 hash of the complete file content

**When any of these changes → cache is automatically invalidated** ✅

### Example

```
Upload: data.csv (100KB)
↓
Cache Key: abc123xyz... (based on name + size + contents)
↓
Process & cache result → Saved to /cache/uploads/
↓
Upload SAME file again
↓
Cache Key: abc123xyz... (IDENTICAL - returns from cache instantly!)
↓
Upload DIFFERENT data (same filename, different contents)
↓
Cache Key: def456uvw... (DIFFERENT - reprocesses & creates new cache)
```

---

## Cache Behavior

### ✅ Cache Hit (File Unchanged)
```
POST /api/batch with "charging_data.csv"
↓
Cache found ✅
↓
Returns cached result in <100ms (no processing)
↓
Logs: "✅ Returning cached result for this file"
```

### ⚠️ Cache Miss (File Changed or New)
```
POST /api/batch with "charging_data.csv" (modified)
↓
Cache key different (content hash changed) ❌
↓
Reprocesses file (new features, predictions, metrics)
↓
Saves new cache entry
↓
Logs: "⚠️ Cache miss - processing file..."
```

---

## Cache Settings

| Setting | Value | Notes |
|---------|-------|-------|
| **TTL (Time-to-Live)** | 1 hour | Cached results expire after 1 hour of inactivity |
| **Storage Location** | `/End_sem/backend/cache/uploads/` | On-disk persistent cache |
| **Max Entries** | Unlimited | Old entries auto-delete after TTL expires |
| **Auto-Pruning** | Every request | Expired entries cleaned up automatically |

---

## API Endpoints

### POST `/api/batch`
**Batch processing with automatic caching**

```bash
curl -X POST http://localhost:8000/api/batch \
  -F "file=@charging_data.csv"
```

**Response includes cache status in logs:**
- `✅ Returning cached result` = Cache hit (fast)
- `⚠️ Cache miss` = Cache miss (processed)

### POST `/api/cache/clear`
**Manually clear all cached results**

```bash
curl -X POST http://localhost:8000/api/cache/clear
```

**Response:**
```json
{
  "status": "success",
  "message": "All cached batch results have been cleared",
  "cache_directory": "/path/to/cache/uploads"
}
```

---

## When to Clear Cache

### Automatically Invalidated When:
✅ File content changes (same filename, different data)  
✅ File size changes  
✅ Cache entry expires (1 hour)  

### Manually Clear Cache When:
- 🔧 Model predictions have changed (retrain)
- 🔄 You want to force re-processing
- 📦 Updating to a new data schema
- 🧹 Cleaning up disk space

**Clear cache:**
```bash
# Option 1: API call
curl -X POST http://localhost:8000/api/cache/clear

# Option 2: Manual deletion
rm -rf End_sem/backend/cache/uploads/*
```

---

## Benefits

| Benefit | Details |
|---------|---------|
| **⚡ Speed** | Instant results for unchanged files |
| **💾 Smart Storage** | Only stores what's needed |
| **🔄 Auto-Invalidation** | No stale data, changes detected automatically |
| **🧹 Auto-Cleanup** | Expires old entries, reclaims disk space |
| **📊 Offline Ready** | Can process without recomputing |

---

## Cache Example Flow

```
Time 1: Upload "data.csv" (100KB)
├─ Cache miss → Process → Save cache
├─ Time taken: 15 seconds
└─ Cache key: abc123xyz...

Time 2: Upload SAME "data.csv" (100KB)
├─ Cache hit → Return cached result
├─ Time taken: <100ms
└─ Logs: "✅ Returning cached result for this file"

Time 3: Upload UPDATED "data.csv" (105KB)
├─ Cache miss → Process → Save cache
├─ Time taken: 15 seconds
└─ Cache key: def456uvw... (NEW, old cache untouched)

Time 4: Cache entry expires (1 hour passed)
├─ Old cache for abc123xyz deleted
├─ Old cache for def456uvw still valid
└─ Auto-pruning happens on next request
```

---

## Logs to Watch For

### Cache Hit ✅
```
Cache key: abc123xyz...
✅ Returning cached result for this file
Batch processing completed: 29905 records, R²=0.891
```

### Cache Miss ⚠️
```
Cache key: abc123xyz...
⚠️ Cache miss - processing file...
Loading model...
Making predictions...
✅ Cached result with key: abc123xyz...
Batch processing completed: 29905 records, R²=0.891
```

### Cache Cleared 🧹
```
POST /api/cache/clear
✅ Cache cleared
All cached batch results have been cleared
```

---

## Performance Impact

### Without Cache
- **First upload:** 15-20 seconds (model load + predictions)
- **Repeat upload:** 15-20 seconds (wasted time!)

### With Cache (This Implementation)
- **First upload:** 15-20 seconds (model load + predictions + cache save)
- **Repeat upload:** <100ms (instant cache hit!)
- **Different file:** 15-20 seconds (cache miss, new entry)

**Result:** ~150x faster for repeated files! ⚡

---

## Troubleshooting

### Q: Cache hit not working?
**A:** Verify file contents haven't changed. Even one byte difference invalidates cache.

```bash
# Check file hash
sha256sum charging_data.csv
```

### Q: Want to force re-processing?
**A:** Clear the cache and reupload.

```bash
curl -X POST http://localhost:8000/api/cache/clear
# Then upload again
```

### Q: How much disk space used?
**A:** Check the cache directory.

```bash
du -sh End_sem/backend/cache/uploads/
```

### Q: Cache entries expired?
**A:** They auto-delete on next request. No action needed.

---

## Advanced: Cache Key Formula

```python
cache_key = SHA256(
    filename.encode() + 
    "|" + 
    str(file_size).encode() + 
    "|" + 
    file_contents
)
```

Same file = Same hash = Cache hit ✅  
Different file = Different hash = Cache miss ✅

---

## Summary

| Feature | Behavior |
|---------|----------|
| **Auto-Invalidation** | Changes detected automatically via content hash |
| **TTL** | 1 hour per cached entry |
| **Manual Clear** | `POST /api/cache/clear` |
| **Performance** | ~150x faster for repeated files |
| **Storage** | On-disk in `/cache/uploads/` |

**Result:** Fast, smart caching that just works! 🚀
