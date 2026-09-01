# Firebase Setup Guide

This guide will help you set up Firebase to replace Supabase for the MaintAI application.

## Step 1: Create Firebase Project

1. **Go to Firebase Console**
   - Visit [console.firebase.google.com](https://console.firebase.google.com)
   - Sign in with your Google account
   - Click "Add project" to create a new project

2. **Configure Project**
   - Project name: `maintai-app` (or your preferred name)
   - Enable Google Analytics: Optional (recommended for production)
   - Select or create a Google Analytics account
   - Click "Create project"

3. **Wait for Project Creation**
   - Firebase will take a minute to provision your project
   - Click "Continue" when ready

## Step 2: Enable Required Firebase Services

### 2.1 Enable Authentication

1. Go to **Build** → **Authentication** in the left sidebar
2. Click **Get Started**
3. Enable **Email/Password** sign-in provider
4. Click **Save**
5. (Optional) Enable other providers as needed

### 2.2 Enable Firestore Database

1. Go to **Build** → **Firestore Database**
2. Click **Create database**
3. Choose a location (select one close to your users)
4. Select **Start in Test Mode** (for development)
5. Click **Enable**

### 2.3 Enable Storage (Optional)

1. Go to **Build** → **Storage**
2. Click **Get Started**
3. Choose security rules: **Start in Test Mode**
4. Select a location (same as Firestore)
5. Click **Enable**

## Step 3: Get Firebase Configuration

1. Go to **Project Settings** (gear icon in left sidebar)
2. Scroll down to **Your apps** section
3. Click **Web** (</>) icon
4. App nickname: `MaintAI Web`
5. Register app
6. Copy the **firebaseConfig** object (you'll need this for environment variables)

The config should look like:
```javascript
const firebaseConfig = {
  apiKey: "AIzaSy...",
  authDomain: "your-project.firebaseapp.com",
  projectId: "your-project-id",
  storageBucket: "your-project.appspot.com",
  messagingSenderId: "123456789",
  appId: "1:123456789:web:abcdef",
  measurementId: "G-XXXXXXXX"
};
```

## Step 4: Configure Environment Variables

1. Copy `.env.example` to `.env.local`:
   ```bash
   cp .env.example .env.local
   ```

2. Fill in your Firebase values:
   ```env
   # Firebase Configuration
   NEXT_PUBLIC_FIREBASE_API_KEY=your-api-key-here
   NEXT_PUBLIC_FIREBASE_AUTH_DOMAIN=your-project.firebaseapp.com
   NEXT_PUBLIC_FIREBASE_PROJECT_ID=your-project-id
   NEXT_PUBLIC_FIREBASE_STORAGE_BUCKET=your-project.appspot.com
   NEXT_PUBLIC_FIREBASE_MESSAGING_SENDER_ID=your-sender-id
   NEXT_PUBLIC_FIREBASE_APP_ID=your-app-id
   NEXT_PUBLIC_FIREBASE_MEASUREMENT_ID=your-measurement-id

   # AI Configuration (Optional - for AI features)
   OPENAI_API_KEY=your-openai-api-key
   AI_PROVIDER=openai
   OPENAI_MODEL=gpt-4o

   # Alternative: Google Gemini (Optional)
   # GEMINI_API_KEY=your-gemini-api-key
   # AI_PROVIDER=gemini
   ```

## Step 5: Create Firestore Collections

### 5.1 Create Collections Manually (via Console)

Go to **Firestore Database** → **Start Collection** and create these collections:

#### `factories` collection
- Document ID: `f0000000-0000-4000-8000-000000000001`
- Fields:
  - `name`: "Apex Manufacturing Plant"
  - `location`: "Pune, Maharashtra, India"

#### `profiles` collection
- Document ID: (auto-generated)
- Fields:
  - `full_name`: "User Name"
  - `email`: "user@example.com"
  - `role`: "technician" | "supervisor" | "admin"
  - `factory_id`: "f0000000-0000-4000-8000-000000000001"
  - `avatar_url`: (optional)

#### `machines` collection
- Document ID: (auto-generated)
- Fields:
  - `name`: "Machine Name"
  - `model`: "Model Number"
  - `manufacturer`: "Manufacturer"
  - `category`: "CNC" | "Pump" | "Compressor" | etc.
  - `qr_code`: "MACHINE:unique-id"
  - `location`: "Bay A - Floor 1"
  - `status`: "operational" | "maintenance" | "broken"
  - `image_url`: (optional)
  - `createdAt`: timestamp

#### `repair_procedures` collection
- Document ID: (auto-generated)
- Fields:
  - `machine_id`: (reference to machine)
  - `procedure_type`: "Oil Change" | "Belt Replacement" | etc.
  - `estimated_minutes`: 30
  - `difficulty`: "Easy" | "Medium" | "Hard"
  - `steps`: array of step objects
  - `createdAt`: timestamp

#### `parts` collection
- Document ID: (auto-generated)
- Fields:
  - `name`: "Part Name"
  - `part_number`: "PART-123"
  - `stock_quantity`: 50
  - `min_stock_level`: 10
  - `unit_price`: 25.00

#### `maintenance_logs` collection
- Document ID: (auto-generated)
- Fields:
  - `machine_id`: (reference to machine)
  - `technician_id`: (reference to profile)
  - `procedure_id`: (reference to procedure)
  - `started_at`: timestamp
  - `completed_at`: timestamp
  - `duration_minutes`: 45
  - `status`: "completed" | "in_progress"
  - `notes`: "Maintenance notes"

#### `fault_reports` collection
- Document ID: (auto-generated)
- Fields:
  - `machine_id`: (reference to machine)
  - `description`: "Fault description"
  - `severity`: "low" | "medium" | "high" | "critical"
  - `status`: "open" | "in_progress" | "resolved"
  - `created_at`: timestamp

### 5.2 Or Import Demo Data (Recommended)

You can use the provided seeding script to automatically populate Firestore with demo data.

1. **Install tsx for running TypeScript scripts:**
   ```bash
   npm install -D tsx
   ```

2. **Run the seeding script:**
   ```bash
   npx tsx scripts/seed-firebase.ts
   ```

This will populate your Firestore with:
- 1 Factory (Apex Manufacturing Plant)
- 5 User Profiles (admin, supervisor, 3 technicians)
- 20 Machines (various types: CNC, pumps, compressors, etc.)
- 10 Parts (with stock levels)
- 50+ Repair Procedures (2-4 per machine)

3. **Create Firebase Auth Users:**
   After seeding, you'll need to manually create the authentication users in Firebase Console:
   - Go to Firebase Console → Authentication → Users
   - Click "Add user" for each account:
     - Email: admin@demo.com, Password: demo123456
     - Email: supervisor@demo.com, Password: demo123456
     - Email: tech1@demo.com, Password: demo123456
     - Email: tech2@demo.com, Password: demo123456
     - Email: tech3@demo.com, Password: demo123456

The user IDs in Firebase Auth will need to match the profile IDs in Firestore. The easiest way is to create the users first, then update the seeding script with the actual Firebase Auth UIDs, or manually update the profile documents in Firestore after creating the users.

## Step 6: Configure Firestore Security Rules

For development, you can use test mode rules. For production, update rules in **Firestore Database** → **Rules**:

```javascript
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    match /{document=**} {
      allow read, write: if request.auth != null;
    }
  }
}
```

## Step 7: Configure Storage Rules (if using Storage)

```javascript
rules_version = '2';
service firebase.storage {
  match /b/{bucket}/o {
    match /{allPaths=**} {
      allow read, write: if request.auth != null;
    }
  }
}
```

## Step 8: Test the Application

1. Restart the development server:
   ```bash
   npm run dev
   ```

2. Open http://localhost:3000

3. Try to sign up with a new account
4. Verify the user is created in Firebase Console → Authentication
5. Check that the profile is created in Firestore → profiles collection

## Step 9: Create Demo Users (Optional)

To create demo users similar to the Supabase version:

1. Go to Firebase Console → Authentication
2. Click **Add user**
3. Create these users (password: `demo123456`):
   - admin@demo.com (Admin role)
   - supervisor@demo.com (Supervisor role)
   - tech1@demo.com (Technician role)

4. Manually create corresponding profile documents in Firestore with the same IDs as the Firebase Auth UIDs

## Migration Notes

### Key Differences from Supabase

1. **Authentication**: Firebase uses email/password by default, Supabase uses similar but with different SDK
2. **Database**: Firestore is NoSQL, Supabase uses PostgreSQL
3. **Real-time**: Both support real-time, but implementation differs
4. **Storage**: Firebase Storage vs Supabase Storage (similar functionality)

### Data Structure Changes

- Firestore uses camelCase field names (e.g., `stock_quantity` vs `stock_quantity`)
- Document IDs are auto-generated by default
- References use different syntax in queries

### API Changes

- All Supabase client calls replaced with Firebase SDK calls
- Middleware uses Firebase auth tokens instead of Supabase session tokens
- Database queries use Firestore syntax instead of SQL

## Troubleshooting

**"Firebase: No Firebase App '[DEFAULT]' has been created"**
- Check that all environment variables are set correctly
- Ensure Firebase configuration is properly initialized

**"Permission denied" errors**
- Check Firestore security rules
- Ensure user is authenticated
- Verify collection names match exactly

**Authentication not working**
- Check that Email/Password provider is enabled
- Verify environment variables are correct
- Check browser console for specific errors

**Demo mode still active**
- Ensure all Firebase environment variables are set
- Check that values don't contain placeholder text like "your-"
- Restart the development server after changing environment variables

## Next Steps

1. Configure proper security rules for production
2. Set up Firebase Analytics for insights
3. Enable Firebase Crashlytics for error tracking
4. Consider Firebase Cloud Functions for server-side logic
5. Set up Firebase Hosting for deployment
