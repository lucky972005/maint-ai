"use client";

import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger } from "@/components/ui/dialog";
import { Upload, X, ChevronLeft, ChevronRight, Star, Camera } from "lucide-react";
import { toast } from "@/hooks/use-toast";

interface ImageManagerProps {
  entityType: "machine" | "part";
  entityId: string;
  existingImages: string[];
  onImagesUpdate: (images: string[]) => void;
  disabled?: boolean;
}

export function ImageManager({ 
  entityType, 
  entityId, 
  existingImages = [], 
  onImagesUpdate,
  disabled = false 
}: ImageManagerProps) {
  const [images, setImages] = useState<string[]>(existingImages);
  const [currentIndex, setCurrentIndex] = useState(0);
  const [uploading, setUploading] = useState(false);
  const [open, setOpen] = useState(false);

  const handleFileUpload = async (event: React.ChangeEvent<HTMLInputElement>) => {
    const files = event.target.files;
    if (!files || files.length === 0) return;

    setUploading(true);
    const newImages: string[] = [];

    try {
      for (let i = 0; i < files.length; i++) {
        const file = files[i];
        const base64 = await fileToBase64(file);
        
        const response = await fetch(`/api/${entityType}s/${entityId}/images`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            images: [{ name: file.name, data: base64 }],
            setPrimaryIndex: images.length + i
          }),
        });

        const data = await response.json();
        if (data.success && data.urls) {
          newImages.push(...data.urls);
        }
      }

      const updatedImages = [...images, ...newImages];
      setImages(updatedImages);
      onImagesUpdate(updatedImages);
      toast({ title: "Success", description: `${newImages.length} image(s) uploaded` });
    } catch (error) {
      console.error("Image upload failed:", error);
      toast({ title: "Upload failed", description: "Could not upload images", variant: "destructive" });
    } finally {
      setUploading(false);
      // Reset file input
      event.target.value = "";
    }
  };

  const handleRemoveImage = async (index: number) => {
    const updatedImages = images.filter((_, i) => i !== index);
    setImages(updatedImages);
    setCurrentIndex(Math.max(0, currentIndex - 1));
    onImagesUpdate(updatedImages);
    
    // Update primary index if needed
    if (index === currentIndex && updatedImages.length > 0) {
      try {
        await fetch(`/api/${entityType}s/${entityId}/images`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ 
            images: [], 
            setPrimaryIndex: 0 
          }),
        });
      } catch (error) {
        console.error("Failed to update primary image:", error);
      }
    }
  };

  const handleSetPrimary = async (index: number) => {
    setCurrentIndex(index);
    try {
      await fetch(`/api/${entityType}s/${entityId}/images`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ 
          images: [], 
          setPrimaryIndex: index 
        }),
      });
      toast({ title: "Primary image updated", description: "Image set as primary" });
    } catch (error) {
      console.error("Failed to set primary image:", error);
    }
  };

  const fileToBase64 = (file: File) =>
    new Promise<string>((resolve, reject) => {
      const reader = new FileReader();
      reader.onload = () => {
        const result = reader.result as string;
        resolve(result.split(",")[1] ?? "");
      };
      reader.onerror = () => reject(new Error("Failed to read file"));
      reader.readAsDataURL(file);
    });

  const navigateImages = (direction: "prev" | "next") => {
    if (images.length === 0) return;
    if (direction === "prev") {
      setCurrentIndex((prev) => (prev - 1 + images.length) % images.length);
    } else {
      setCurrentIndex((prev) => (prev + 1) % images.length);
    }
  };

  return (
    <Dialog open={open} onOpenChange={setOpen}>
      <DialogTrigger asChild>
        <Button variant="outline" size="sm" disabled={disabled}>
          <Camera className="h-4 w-4 mr-2" />
          Manage Images ({images.length})
        </Button>
      </DialogTrigger>
      <DialogContent className="max-w-2xl">
        <DialogHeader>
          <DialogTitle>Manage {entityType} Images</DialogTitle>
        </DialogHeader>
        
        <div className="space-y-4">
          {/* Image Gallery */}
          {images.length > 0 ? (
            <Card>
              <CardContent className="p-4">
                <div className="relative aspect-video bg-muted rounded-lg overflow-hidden">
                  <img
                    src={images[currentIndex]}
                    alt={`${entityType} image ${currentIndex + 1}`}
                    className="w-full h-full object-contain"
                  />
                  
                  {images.length > 1 && (
                    <>
                      <button
                        onClick={() => navigateImages("prev")}
                        className="absolute left-2 top-1/2 -translate-y-1/2 p-2 bg-black/50 hover:bg-black/70 rounded-full text-white transition"
                      >
                        <ChevronLeft className="h-4 w-4" />
                      </button>
                      <button
                        onClick={() => navigateImages("next")}
                        className="absolute right-2 top-1/2 -translate-y-1/2 p-2 bg-black/50 hover:bg-black/70 rounded-full text-white transition"
                      >
                        <ChevronRight className="h-4 w-4" />
                      </button>
                      <div className="absolute bottom-2 left-1/2 -translate-x-1/2 flex gap-1">
                        {images.map((_, i) => (
                          <button
                            key={i}
                            onClick={() => setCurrentIndex(i)}
                            className={`w-2 h-2 rounded-full transition ${i === currentIndex ? 'bg-white' : 'bg-white/50'}`}
                          />
                        ))}
                      </div>
                    </>
                  )}
                  
                  <button
                    onClick={() => handleRemoveImage(currentIndex)}
                    className="absolute top-2 right-2 p-2 bg-red-500/80 hover:bg-red-600 rounded-full text-white transition"
                  >
                    <X className="h-4 w-4" />
                  </button>
                  
                  <button
                    onClick={() => handleSetPrimary(currentIndex)}
                    className="absolute top-2 left-2 p-2 bg-black/50 hover:bg-black/70 rounded-full text-white transition"
                    title="Set as primary image"
                  >
                    <Star className={`h-4 w-4 ${currentIndex === 0 ? 'text-yellow-400 fill-yellow-400' : ''}`} />
                  </button>
                </div>
                
                <div className="mt-3 flex items-center justify-between text-sm text-muted-foreground">
                  <span>Image {currentIndex + 1} of {images.length}</span>
                  {currentIndex === 0 && (
                    <Badge variant="secondary">Primary</Badge>
                  )}
                </div>
              </CardContent>
            </Card>
          ) : (
            <Card>
              <CardContent className="p-8 text-center">
                <Camera className="h-12 w-12 mx-auto mb-3 text-muted-foreground" />
                <p className="text-muted-foreground">No images uploaded yet</p>
              </CardContent>
            </Card>
          )}

          {/* Upload Button */}
          <label>
            <input
              type="file"
              accept="image/*"
              multiple
              className="hidden"
              onChange={handleFileUpload}
              disabled={uploading}
            />
            <Button variant="outline" className="w-full" asChild disabled={uploading}>
              <span>
                <Upload className="h-4 w-4 mr-2" />
                {uploading ? "Uploading..." : "Upload Images"}
              </span>
            </Button>
          </label>

          {/* Thumbnail Grid */}
          {images.length > 0 && (
            <div className="grid grid-cols-4 gap-2">
              {images.map((img, i) => (
                <div
                  key={i}
                  className={`relative aspect-square rounded-lg overflow-hidden cursor-pointer border-2 transition ${
                    i === currentIndex ? 'border-primary' : 'border-transparent hover:border-border'
                  }`}
                  onClick={() => setCurrentIndex(i)}
                >
                  <img src={img} alt={`Thumbnail ${i + 1}`} className="w-full h-full object-cover" />
                  {i === 0 && (
                    <div className="absolute top-1 left-1">
                      <Star className="h-3 w-3 text-yellow-400 fill-yellow-400" />
                    </div>
                  )}
                </div>
              ))}
            </div>
          )}
        </div>
      </DialogContent>
    </Dialog>
  );
}
