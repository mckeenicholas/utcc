<script lang="ts">
import "../app.css";
import { afterNavigate } from "$app/navigation";
import { page } from "$app/state";
import Footer from "$lib/components/Footer.svelte";
import Navbar from "$lib/components/Navbar.svelte";
import { incrementNavigationCount } from "$lib/stores/navigation";

const { children } = $props();

afterNavigate(incrementNavigationCount);

const isHomePage = $derived(page.url.pathname === "/");
</script>

<div class="flex min-h-screen flex-col bg-gray-50 text-gray-900 antialiased">
	{#if !isHomePage}
		<Navbar />
	{/if}
	<main class="flex-1">
		{@render children()}
	</main>
	<Footer />
</div>
