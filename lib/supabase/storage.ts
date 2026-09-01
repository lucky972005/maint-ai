import { createClient } from "./client";

const supabase = createClient();

export async function uploadFile(path: string, buffer: Buffer): Promise<string> {
  const { data, error } = await supabase.storage
    .from("evidence")
    .upload(path, buffer, {
      contentType: "image/jpeg",
      upsert: true,
    });

  if (error) throw error;

  const { data: { publicUrl } } = supabase.storage
    .from("evidence")
    .getPublicUrl(data.path);

  return publicUrl;
}

export async function deleteFile(path: string): Promise<void> {
  const { error } = await supabase.storage
    .from("evidence")
    .remove([path]);

  if (error) throw error;
}
