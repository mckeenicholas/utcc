<script lang="ts">
import { onMount } from "svelte";
import CubeIcon from "$lib/components/CubeIcon.svelte";
import ThemeToggle from "$lib/components/ThemeToggle.svelte";
import { type Competition, type Paginated } from "$lib/types";
import { fetchJson, formatCompetitionDate, latestCompetitionsURL } from "$lib/utils";

let latestCompetition: Competition | null = $state(null);
let upcomingCompetitions: Competition[] = $state([]);
let loadingData = $state(true);

const directorySections = [
	{
		href: "/results",
		title: "Official Results",
		subtitle: "Latest competition results",
		icon: "event-333",
		action: "View Results",
	},
	{
		href: "/records",
		title: "Club Records",
		subtitle: "View the best results achieved at UTRCC competitions",
		icon: "event-444",
		action: "View Records",
	},
	{
		href: "/rankings",
		title: "Leaderboards",
		subtitle: "View current event standings",
		icon: "event-pyram",
		action: "View Rankings",
	},
	{
		href: "/competitions",
		title: "Competitions",
		subtitle: "Browse past competitions and scramble logs",
		icon: "event-sq1",
		action: "Browse Archive",
	},
	{
		href: "/persons",
		title: "Competitors",
		subtitle: "View individual member results",
		icon: "event-minx",
		action: "Find Solvers",
	},
] as const;

onMount(async () => {
	try {
		loadingData = true;
		const [latestData, upcomingData] = await Promise.allSettled([
			fetchJson<Paginated<Competition>>(`${latestCompetitionsURL}?has_results=true`),
			fetchJson<Paginated<Competition>>(`${latestCompetitionsURL}?upcoming=true`),
		]);

		if (latestData.status === "fulfilled" && latestData.value.results?.length > 0) {
			latestCompetition =
				latestData.value.results.find((comp) => (comp.events && comp.events.length > 0) || comp.has_results) ?? null;
		}

		if (upcomingData.status === "fulfilled" && upcomingData.value.results?.length > 0) {
			upcomingCompetitions = upcomingData.value.results;
		}
	} catch (error) {
		console.error("Error loading homepage live data:", error);
	} finally {
		loadingData = false;
	}
});
</script>

<svelte:head>
	<title>U of T Cube Club | Official Results, Records & Competitions</title>
	<meta
		name="description"
		content="Official results, club records, and member rankings for the University of Toronto Rubik's Cube Club."
	/>
</svelte:head>

<div class="relative py-10 sm:py-14">
	<!-- Top-right corner theme toggle (outside max-w-6xl column on wide monitors) -->
	<div class="absolute top-4 right-4 sm:top-6 sm:right-6 lg:top-8 lg:right-8">
		<ThemeToggle />
	</div>

	<div class="mx-auto max-w-6xl px-4 sm:px-6">
		<!-- Hero Section: Logo Crest & Club Title Lockup -->
		<div class="flex flex-col justify-between gap-6 border-b border-border pb-10 sm:flex-row sm:items-center">
			<div class="flex items-center gap-6 pr-12 sm:gap-8 sm:pr-0">
				<img
					src="/client-static/logo.png"
					alt="University of Toronto Cube Club Crest"
					class="h-28 w-28 shrink-0 object-contain sm:h-36 sm:w-36"
					loading="eager"
				/>

				<div>
					<h1 class="text-3xl font-bold tracking-tight text-brand sm:text-4xl lg:text-5xl">
						University of Toronto Cube Club
					</h1>
				</div>
			</div>
		</div>

		<!-- Card 1: Unified Directory Matrix (Architectural Navigation Strip) -->
		<div
			class="mt-4 grid grid-cols-1 divide-y divide-border border border-border bg-surface md:grid-cols-5 md:divide-x md:divide-y-0"
		>
			{#each directorySections as section (section.href)}
				<a href={section.href} class="group flex flex-col justify-between p-5 transition-colors hover:bg-surface-muted">
					<div>
						<div class="flex items-center justify-between">
							<span class="cubing-icon {section.icon} text-lg text-brand transition-transform group-hover:scale-110"
							></span>
							<svg
								class="h-4 w-4 text-muted transition-transform group-hover:translate-x-0.5 group-hover:text-brand"
								fill="none"
								stroke="currentColor"
								viewBox="0 0 24 24"
							>
								<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
							</svg>
						</div>
						<h3 class="mt-4 text-sm font-bold text-main transition-colors group-hover:text-brand">
							{section.title}
						</h3>
						<p class="mt-1 text-xs leading-relaxed text-secondary">
							{section.subtitle}
						</p>
					</div>

					<div
						class="mt-6 border-t border-border pt-3 text-xs font-semibold text-brand transition-colors group-hover:text-secondary-cyan"
					>
						{section.action} &rarr;
					</div>
				</a>
			{/each}
		</div>

		<!-- Card 2: Live / Recent Competition Editorial Strip -->
		<div class="mt-8">
			{#if latestCompetition}
				<div class="border border-border bg-surface">
					<div
						class="flex flex-col gap-4 border-b border-border bg-surface-subtle px-5 py-3 sm:flex-row sm:items-center sm:justify-between"
					>
						<div class="flex items-center gap-3">
							<span
								class="rounded-sm bg-uoft-blue px-2 py-0.5 text-[10px] font-bold tracking-wider text-white uppercase dark:border dark:border-blue-500/40"
							>
								Latest Competition
							</span>
							<span class="text-xs font-semibold text-main">
								{latestCompetition.name}
							</span>
						</div>
						<div class="flex items-center gap-4 text-xs text-secondary">
							<span class="tabular-nums">{formatCompetitionDate(latestCompetition.date)}</span>
							{#if latestCompetition.student_designator}
								<span class="rounded-sm bg-surface-muted px-1.5 py-0.5 text-[10px] font-semibold text-secondary">
									{latestCompetition.student_designator}
								</span>
							{/if}
						</div>
					</div>

					<div class="flex flex-col gap-4 p-5 sm:flex-row sm:items-center sm:justify-between">
						<div class="flex flex-wrap items-center gap-2">
							<span class="text-xs font-medium text-secondary">Events:</span>
							<div class="flex flex-wrap items-center gap-1.5">
								{#each latestCompetition.events as ev (ev)}
									<CubeIcon event={ev} class="text-base text-secondary transition-colors hover:text-brand" />
								{/each}
							</div>
						</div>

						<a
							href="/competitions/{latestCompetition.id}"
							class="inline-flex shrink-0 items-center gap-2 rounded-sm bg-uoft-blue px-4 py-2 text-xs font-medium text-white transition-colors hover:bg-uoft-blue-80 dark:border dark:border-blue-500/30"
						>
							View Results &rarr;
						</a>
					</div>
				</div>
			{:else if loadingData}
				<div class="animate-pulse border border-border bg-surface p-5">
					<div class="flex items-center justify-between">
						<div class="h-4 w-40 rounded-sm bg-surface-muted"></div>
						<div class="h-4 w-24 rounded-sm bg-surface-muted"></div>
					</div>
					<div class="mt-4 h-6 w-64 rounded-sm bg-surface-muted"></div>
				</div>
			{:else}
				<div class="border border-border bg-surface p-6 text-center">
					<p class="text-sm text-secondary">Unable to load results</p>
				</div>
			{/if}
		</div>

		<!-- Card 3: Upcoming Competitions Card -->
		<div class="mt-6">
			{#if upcomingCompetitions.length > 0}
				<div class="divide-y divide-border border border-border bg-surface">
					{#each upcomingCompetitions as upcomingComp (upcomingComp.id)}
						<div>
							<div
								class="flex flex-col gap-4 border-b border-border bg-surface-subtle px-5 py-3 sm:flex-row sm:items-center sm:justify-between"
							>
								<div class="flex items-center gap-3">
									<span
										class="rounded-sm bg-secondary-cyan px-2 py-0.5 text-[10px] font-bold tracking-wider text-white uppercase dark:bg-secondary-cyan/80"
									>
										Upcoming Competition
									</span>
									<span class="text-xs font-semibold text-main">
										{upcomingComp.name}
									</span>
								</div>
								<div class="flex items-center gap-4 text-xs text-secondary">
									<span class="font-medium text-secondary tabular-nums">{formatCompetitionDate(upcomingComp.date)}</span
									>
									{#if upcomingComp.student_designator}
										<span class="rounded-sm bg-surface-muted px-1.5 py-0.5 text-[10px] font-semibold text-secondary">
											{upcomingComp.student_designator}
										</span>
									{/if}
								</div>
							</div>

							<div class="flex flex-col gap-4 p-5 sm:flex-row sm:items-center sm:justify-between">
								<div class="flex flex-wrap items-center gap-2">
									<span class="text-xs font-medium text-secondary">Events:</span>
									<div class="flex flex-wrap items-center gap-1.5">
										{#if upcomingComp.events && upcomingComp.events.length > 0}
											{#each upcomingComp.events as ev (ev)}
												<CubeIcon event={ev} class="text-base text-secondary transition-colors hover:text-brand" />
											{/each}
										{:else}
											<span class="text-xs text-muted italic">TBD</span>
										{/if}
									</div>
								</div>

								<a
									href="/competitions/{upcomingComp.id}"
									class="inline-flex shrink-0 items-center gap-2 rounded-sm border border-uoft-blue bg-surface px-4 py-2 text-xs font-medium text-brand transition-colors hover:bg-uoft-blue hover:text-white dark:border-blue-400 dark:hover:bg-blue-600"
								>
									View Details &rarr;
								</a>
							</div>
						</div>
					{/each}
				</div>
			{:else if loadingData}
				<div class="animate-pulse border border-border bg-surface p-5">
					<div class="flex items-center justify-between">
						<div class="h-4 w-40 rounded-sm bg-surface-muted"></div>
						<div class="h-4 w-24 rounded-sm bg-surface-muted"></div>
					</div>
					<div class="mt-4 h-6 w-64 rounded-sm bg-surface-muted"></div>
				</div>
			{:else}
				<div class="border border-border bg-surface p-6 text-center">
					<p class="text-sm text-secondary">Unable to load upcoming competitions</p>
				</div>
			{/if}
		</div>
	</div>
</div>
