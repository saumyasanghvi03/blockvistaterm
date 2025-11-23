# Implementation Plan - Missing Pages & Legal Section

This plan outlines the steps to create the missing pages and the common legal information page for BlockVista Terminal.

## User Review Required

> [!IMPORTANT]
> I will create a single `Legal` page that contains sections for Privacy, Terms, and Compliance. `Security` will be a standalone page as it is also listed under "Product".

## Proposed Changes

### 1. Create New Page Components
I will create the following files in `src/pages/`:

-   **`Features.tsx`**: Detailed breakdown of platform features.
-   **`Security.tsx`**: Information about security measures (encryption, 2FA, etc.).
-   **`ApiDocs.tsx`**: Documentation landing page or API reference.
-   **`Blog.tsx`**: A list of blog posts (mocked for now).
-   **`Careers.tsx`**: Job openings and company culture.
-   **`Legal.tsx`**: A tabbed or sectioned page containing:
    -   Privacy Policy
    -   Terms of Service
    -   Compliance Info

### 2. Update Routing (`App.tsx`)
Add the following routes:
-   `/features` -> `Features`
-   `/security` -> `Security`
-   `/api-docs` -> `ApiDocs`
-   `/blog` -> `Blog`
-   `/careers` -> `Careers`
-   `/legal` -> `Legal`

### 3. Update Footer (`src/components/Footer.tsx`)
Update the `href` attributes to point to the new routes instead of `#`.

## Verification Plan

### Automated Tests
-   None (Visual verification).

### Manual Verification
-   Click each link in the Footer and Navbar.
-   Verify the content of each new page renders correctly.
-   Check the "Legal" page allows navigation between its sections (Privacy, Terms, etc.).
