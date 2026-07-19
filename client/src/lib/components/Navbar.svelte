<script lang="ts">
import { onMount } from "svelte";
import { page } from "$app/state";
import { checkLoginStatus } from "$lib/utils";

let isLoggedIn = $state(false);

onMount(async () => {
	try {
		isLoggedIn = await checkLoginStatus();
	} catch {
		isLoggedIn = false;
	}
});

const navLinks = [
	{ label: "Results", href: "/results" },
	{ label: "Records", href: "/records" },
	{ label: "Rankings", href: "/rankings" },
	{ label: "Competitions", href: "/competitions" },
	{ label: "Competitors", href: "/persons" },
];

const isActive = (href: string) => {
	const currentPath = page.url.pathname;
	if (href === "/") {
		return currentPath === "/";
	}
	return currentPath.startsWith(href);
};
</script>

<header class="sticky top-0 z-40 w-full border-b border-gray-200 bg-white/95 shadow-sm backdrop-blur-md">
	<div class="mx-auto flex h-16 max-w-6xl items-center justify-between px-4 sm:px-6 lg:px-8">
		<!-- Brand Logo -->
		<a href="/" class="group flex items-center space-x-3">
			<div class="grid h-6 w-6 rotate-12 grid-cols-2 gap-0.5 transition-transform duration-300 group-hover:rotate-45">
				<div class="rounded-sm bg-red-500"></div>
				<div class="rounded-sm bg-blue-600"></div>
				<div class="rounded-sm bg-amber-400"></div>
				<div class="rounded-sm bg-emerald-500"></div>
			</div>
			<span class="text-lg font-bold tracking-tight text-gray-900 sm:text-xl">
				UofT <span class="text-blue-600">Cube Club</span>
			</span>
		</a>

		<!-- Desktop Navigation -->
		<nav class="hidden space-x-1 md:flex lg:space-x-2">
			{#each navLinks as link}
				<a
					href={link.href}
					class="rounded-lg px-3 py-2 text-sm font-medium transition-colors
						{isActive(link.href) ? 'bg-blue-50 text-blue-600' : 'text-gray-600 hover:bg-gray-50 hover:text-gray-900'}"
				>
					{link.label}
				</a>
			{/each}
		</nav>

		<!-- Right Side (Dashboard / Auth) -->
		<div class="flex items-center space-x-2">
			{#if isLoggedIn}
				<a
					href="/dashboard"
					class="inline-flex items-center justify-center rounded-lg bg-blue-600 px-4 py-2 text-sm font-semibold text-white shadow-sm transition-colors hover:bg-blue-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-blue-600"
				>
					Dashboard
				</a>
				<a
					href="/dashboard/signout"
					class="hidden items-center justify-center rounded-lg border border-gray-200 bg-white px-3 py-2 text-sm font-medium text-gray-700 shadow-sm transition-colors hover:bg-gray-50 sm:inline-flex"
				>
					Sign Out
				</a>
			{:else}
				<a
					href="/dashboard/signin"
					class="inline-flex items-center justify-center rounded-lg border border-gray-200 bg-white px-4 py-2 text-sm font-semibold text-gray-700 shadow-sm transition-colors hover:bg-gray-50"
				>
					Sign In
				</a>
			{/if}
		</div>
	</div>

	<!-- Mobile Sub-Navigation -->
	<div
		class="flex scrollbar-none gap-1 overflow-x-auto border-t border-gray-100 bg-gray-50/50 px-4 py-2 whitespace-nowrap md:hidden"
	>
		{#each navLinks as link}
			<a
				href={link.href}
				class="inline-block rounded-md px-3 py-1.5 text-xs font-semibold transition-colors
					{isActive(link.href) ? 'bg-blue-600 text-white shadow-sm' : 'text-gray-600 hover:bg-gray-100 hover:text-gray-900'}"
			>
				{link.label}
			</a>
		{/each}
	</div>
</header>
