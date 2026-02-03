# PROJECT IDEAS

&nbsp;

## General Project Idea

### UI

> - **First screen:** Ask the user for the interface type. **_Modern_** or **_expert_** version. See below.
> - **Second screen:** Ask for a destination path for the downloads.
> - **_Specification of the different interfaces_:**
>
> 1. **Modern version**
>    - This version relies on using a cache and IGDB (API key not provided) to scrape data in real-time (and cache it).
>    - This version should be as clean as possible, while still being feature-complete (using transitions and widget hiding).
>    - When a game is selected, show the different available versions in a dedicated panel (if applicable).
> 2. **Expert version**:
>    - Offers a version similar to the old program, in the form of a raw table with a list of platforms on the left, a search bar at the top, and a region selector.
>    - No frills, just the raw data!
>    - Allows for multiple ROM selection, sorting by size, weight, etc.

### Backend

> 1. Mandatory caching system
> 2. Fetch IGDB metadata for the modern version
> 3. Prioritize Archive.org, but have Erista as a backup (choice details to be determined).
