# How to Deploy BlockVista Terminal to blockvista.in

Since you have a custom domain (`blockvista.in`), the best way to host your React/Vite application is using a modern static hosting provider like **Vercel** or **Netlify**. They are free, fast, and make SSL (HTTPS) setup automatic.

## Option 1: Deploy using Vercel (Recommended)

Vercel is optimized for frontend frameworks and is the easiest to set up.

### 1. Create a GitHub Repository
1.  Go to [GitHub.com](https://github.com) and create a new repository named `blockvista-terminal`.
2.  Push your code to GitHub:
    ```bash
    git init
    git add .
    git commit -m "Initial commit"
    git branch -M main
    git remote add origin https://github.com/YOUR_USERNAME/blockvista-terminal.git
    git push -u origin main
    ```

### 2. Connect to Vercel
1.  Go to [Vercel.com](https://vercel.com) and sign up/login.
2.  Click **"Add New..."** -> **"Project"**.
3.  Select your `blockvista-terminal` repository.
4.  Vercel will detect it's a Vite project. Keep default settings and click **Deploy**.
5.  Wait for the build to finish. You will get a `blockvista-terminal.vercel.app` URL.

### 3. Connect Your Domain (blockvista.in)
1.  In your Vercel project dashboard, go to **Settings** -> **Domains**.
2.  Enter `blockvista.in` and click **Add**.
3.  Select the option to add `www.blockvista.in` as well if prompted.
4.  Vercel will show you **DNS Records** to add.

### 4. Update DNS Records
Go to your domain registrar (where you bought `blockvista.in`, e.g., GoDaddy, Namecheap, BigRock) and manage DNS settings:

| Type | Name | Value |
|------|------|-------|
| A    | @    | 76.76.21.21 |
| CNAME| www  | cname.vercel-dns.com |

*Note: It might take up to 24-48 hours for DNS to propagate, but usually it's within minutes.*

---

## Option 2: Deploy using Netlify (Alternative)

### 1. Drag & Drop Deployment (Easiest, no Git needed)
1.  Run the build command in your terminal:
    ```bash
    npm run build
    ```
2.  This creates a `dist` folder in your project directory.
3.  Go to [Netlify.com](https://netlify.com) and sign up.
4.  Drag and drop the `dist` folder into the Netlify dashboard.
5.  Your site is now live on a random Netlify URL.

### 2. Connect Custom Domain
1.  Click **"Domain settings"** -> **"Add custom domain"**.
2.  Enter `blockvista.in`.
3.  Click **"Verify"** -> **"Yes, add domain"**.
4.  Netlify will show DNS records.

### 3. Update DNS Records
Login to your domain registrar and add:

| Type | Name | Value |
|------|------|-------|
| A    | @    | 75.2.60.5 |
| CNAME| www  | blockvista-terminal.netlify.app |

*(Check Netlify dashboard for the exact IP address as it can change)*

---

## ✅ Pre-Deployment Checklist

I have already run the build for you, and it passed successfully!

- [x] **Build Success**: `npm run build` completed without errors.
- [x] **Environment Variables**: No sensitive backend keys are needed anymore (Supabase removed).
- [x] **Links**: All "Request Demo" buttons point to your JotForm agent.
- [x] **Assets**: Images and fonts are optimized.

Your `dist` folder is ready for deployment!
