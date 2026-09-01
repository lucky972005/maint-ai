import { 
  signInWithEmailAndPassword, 
  createUserWithEmailAndPassword,
  signOut as firebaseSignOut,
  onAuthStateChanged,
  User as FirebaseUser,
  updateProfile,
} from "firebase/auth";
import { auth } from "../firebase";
import type { UserRole } from "../types";

function setAuthCookie(token: string) {
  if (typeof document === "undefined") return;
  const secure = window.location.protocol === "https:" ? "; secure" : "";
  document.cookie = `firebase-auth-token=${token}; path=/; max-age=3600; samesite=lax${secure}`;
}

function clearAuthCookie() {
  if (typeof document === "undefined") return;
  document.cookie = "firebase-auth-token=; path=/; max-age=0; samesite=lax";
}

export async function signIn(email: string, password: string) {
  const userCredential = await signInWithEmailAndPassword(auth, email, password);
  const token = await userCredential.user.getIdToken();
  setAuthCookie(token);
  return userCredential.user;
}

export async function signUp(email: string, password: string, fullName: string, role: UserRole) {
  const userCredential = await createUserWithEmailAndPassword(auth, email, password);
  
  await updateProfile(userCredential.user, {
    displayName: fullName,
  });

  const token = await userCredential.user.getIdToken();
  setAuthCookie(token);
  
  const { createProfile } = await import("./database");
  await createProfile({
    id: userCredential.user.uid,
    full_name: fullName,
    email: email,
    role: role,
    factory_id: "f0000000-0000-4000-8000-000000000001",
    avatar_url: null,
  });
  
  return userCredential.user;
}

export async function signOut() {
  clearAuthCookie();
  await firebaseSignOut(auth);
}

export function onAuthStateChange(callback: (user: FirebaseUser | null) => void) {
  return onAuthStateChanged(auth, callback);
}

export function getCurrentUser(): FirebaseUser | null {
  return auth.currentUser;
}

export async function getCurrentUserId(): Promise<string | null> {
  const user = auth.currentUser;
  return user ? user.uid : null;
}

export async function getAuthToken(): Promise<string | null> {
  const user = auth.currentUser;
  if (!user) return null;
  return await user.getIdToken();
}
