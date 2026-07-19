<script lang="ts">
import "../app.css";
import { afterNavigate } from "$app/navigation";
import Navbar from "$lib/components/Navbar.svelte";
import { incrementNavigationCount } from "$lib/stores/navigation";

const { children } = $props();

afterNavigate(incrementNavigationCount);
</script>

<Navbar />
{@render children()}
