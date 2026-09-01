<script lang="ts">
import { onMount } from "svelte";
import CubeIcon from "$lib/components/CubeIcon.svelte";
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

<div class="py-10 sm:py-14">
	<div class="mx-auto max-w-6xl px-4 sm:px-6">
		<!-- Hero Section: Logo Crest & Club Title Lockup -->
		<div class="border-b border-gray-200 pb-10">
			<div class="flex items-center gap-6 sm:gap-8">
				<img
					src="/client-static/logo.png"
					alt="University of Toronto Cube Club Crest"
					class="h-28 w-28 shrink-0 object-contain sm:h-36 sm:w-36"
					loading="eager"
				/>

				<div>
					<h1 class="text-3xl font-bold tracking-tight text-uoft-blue sm:text-4xl lg:text-5xl">
						University of Toronto Cube Club
					</h1>
				</div>
			</div>
		</div>

		<!-- Card 1: Unified Directory Matrix (Architectural Navigation Strip) -->
		<div
			class="mt-4 grid grid-cols-1 divide-y divide-gray-200 border border-gray-200 bg-white md:grid-cols-5 md:divide-x md:divide-y-0"
		>
			{#each directorySections as section (section.href)}
				<a href={section.href} class="group flex flex-col justify-between p-5 transition-colors hover:bg-gray-50/80">
					<div>
						<div class="flex items-center justify-between">
							<span class="cubing-icon {section.icon} text-lg text-uoft-blue transition-transform group-hover:scale-110"
							></span>
							<svg
								class="h-4 w-4 text-gray-400 transition-transform group-hover:translate-x-0.5 group-hover:text-uoft-blue"
								fill="none"
								stroke="currentColor"
								viewBox="0 0 24 24"
							>
								<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
							</svg>
						</div>
						<h3 class="mt-4 text-sm font-bold text-gray-900 transition-colors group-hover:text-uoft-blue">
							{section.title}
						</h3>
						<p class="mt-1 text-xs leading-relaxed text-gray-700">
							{section.subtitle}
						</p>
					</div>

					<div
						class="mt-6 border-t border-gray-100 pt-3 text-xs font-semibold text-uoft-blue transition-colors group-hover:text-secondary-cyan"
					>
						{section.action} &rarr;
					</div>
				</a>
			{/each}
		</div>

		<!-- Card 2: Live / Recent Competition Editorial Strip -->
		<div class="mt-8">
			{#if latestCompetition}
				<div class="border border-gray-200 bg-white">
					<div
						class="flex flex-col gap-4 border-b border-gray-100 bg-gray-50/70 px-5 py-3 sm:flex-row sm:items-center sm:justify-between"
					>
						<div class="flex items-center gap-3">
							<span
								class="rounded-sm bg-uoft-blue px-2 py-0.5 text-[10px] font-bold tracking-wider text-white uppercase"
							>
								Latest Competition
							</span>
							<span class="text-xs font-semibold text-gray-700">
								{latestCompetition.name}
							</span>
						</div>
						<div class="flex items-center gap-4 text-xs text-gray-700">
							<span class="tabular-nums">{formatCompetitionDate(latestCompetition.date)}</span>
							{#if latestCompetition.student_designator}
								<span class="rounded-sm bg-gray-200 px-1.5 py-0.5 text-[10px] font-semibold text-gray-700">
									{latestCompetition.student_designator}
								</span>
							{/if}
						</div>
					</div>

					<div class="flex flex-col gap-4 p-5 sm:flex-row sm:items-center sm:justify-between">
						<div class="flex flex-wrap items-center gap-2">
							<span class="text-xs font-medium text-gray-700">Events:</span>
							<div class="flex flex-wrap items-center gap-1.5">
								{#each latestCompetition.events as ev (ev)}
									<CubeIcon event={ev} class="text-base text-gray-700 transition-colors hover:text-uoft-blue" />
								{/each}
							</div>
						</div>

						<a
							href="/competitions/{latestCompetition.id}"
							class="inline-flex shrink-0 items-center gap-2 rounded-sm bg-uoft-blue px-4 py-2 text-xs font-medium text-white transition-colors hover:bg-uoft-blue-80"
						>
							View Results &rarr;
						</a>
					</div>
				</div>
			{:else if loadingData}
				<div class="animate-pulse border border-gray-200 bg-white p-5">
					<div class="flex items-center justify-between">
						<div class="h-4 w-40 rounded-sm bg-gray-200"></div>
						<div class="h-4 w-24 rounded-sm bg-gray-200"></div>
					</div>
					<div class="mt-4 h-6 w-64 rounded-sm bg-gray-200"></div>
				</div>
			{:else}
				<!-- Fallback Notice when no competitions are found -->
				<div
					class="flex flex-col items-start justify-between gap-4 border border-gray-200 bg-white p-5 sm:flex-row sm:items-center"
				>
					<div>
						<div class="flex items-center gap-2">
							<span
								class="rounded-sm bg-uoft-blue px-2 py-0.5 text-[10px] font-bold tracking-wider text-white uppercase"
							>
								Official Archive
							</span>
							<span class="text-xs font-medium text-gray-700">University of Toronto Competitions</span>
						</div>
						<h2 class="mt-1 text-base font-bold text-gray-900">Explore Club Tournaments & Scramble Records</h2>
						<p class="mt-1 text-xs text-gray-600">
							Browse historical solve times, round-by-round rankings, and certified TNoodle scrambles.
						</p>
					</div>
					<a
						href="/competitions"
						class="inline-flex shrink-0 items-center gap-2 rounded-sm bg-uoft-blue px-4 py-2 text-xs font-medium text-white transition-colors hover:bg-uoft-blue-80"
					>
						Browse Competitions &rarr;
					</a>
				</div>
			{/if}
		</div>

		<!-- Card 3: Upcoming Competitions Card -->
		<div class="mt-6">
			{#if upcomingCompetitions.length > 0}
				<div class="divide-y divide-gray-100 border border-gray-200 bg-white">
					{#each upcomingCompetitions as upcomingComp (upcomingComp.id)}
						<div>
							<div
								class="flex flex-col gap-4 border-b border-gray-100 bg-gray-50/70 px-5 py-3 sm:flex-row sm:items-center sm:justify-between"
							>
								<div class="flex items-center gap-3">
									<span
										class="rounded-sm bg-secondary-cyan px-2 py-0.5 text-[10px] font-bold tracking-wider text-white uppercase"
									>
										Upcoming Competition
									</span>
									<span class="text-xs font-semibold text-gray-900">
										{upcomingComp.name}
									</span>
								</div>
								<div class="flex items-center gap-4 text-xs text-gray-700">
									<span class="font-medium text-gray-700 tabular-nums">{formatCompetitionDate(upcomingComp.date)}</span>
									{#if upcomingComp.student_designator}
										<span class="rounded-sm bg-gray-200 px-1.5 py-0.5 text-[10px] font-semibold text-gray-700">
											{upcomingComp.student_designator}
										</span>
									{/if}
								</div>
							</div>

							<div class="flex flex-col gap-4 p-5 sm:flex-row sm:items-center sm:justify-between">
								<div class="flex flex-wrap items-center gap-2">
									<span class="text-xs font-medium text-gray-700">Events:</span>
									<div class="flex flex-wrap items-center gap-1.5">
										{#if upcomingComp.events && upcomingComp.events.length > 0}
											{#each upcomingComp.events as ev (ev)}
												<CubeIcon event={ev} class="text-base text-gray-700 transition-colors hover:text-uoft-blue" />
											{/each}
										{:else}
											<span class="text-xs text-gray-500 italic">TBD</span>
										{/if}
									</div>
								</div>

								<a
									href="/competitions/{upcomingComp.id}"
									class="inline-flex shrink-0 items-center gap-2 rounded-sm border border-uoft-blue bg-white px-4 py-2 text-xs font-medium text-uoft-blue transition-colors hover:bg-uoft-blue hover:text-white"
								>
									View Details &rarr;
								</a>
							</div>
						</div>
					{/each}
				</div>
			{:else if loadingData}
				<div class="animate-pulse border border-gray-200 bg-white p-5">
					<div class="flex items-center justify-between">
						<div class="h-4 w-40 rounded-sm bg-gray-200"></div>
						<div class="h-4 w-24 rounded-sm bg-gray-200"></div>
					</div>
					<div class="mt-4 h-6 w-64 rounded-sm bg-gray-200"></div>
				</div>
			{:else}
				<!-- Empty State when no upcoming competitions are scheduled -->
				<div
					class="flex flex-col items-start justify-between gap-4 border border-gray-200 bg-white p-5 sm:flex-row sm:items-center"
				>
					<div>
						<div class="flex items-center gap-2">
							<span
								class="rounded-sm bg-secondary-cyan px-2 py-0.5 text-[10px] font-bold tracking-wider text-white uppercase"
							>
								Upcoming Competitions
							</span>
							<span class="text-xs font-medium text-gray-700">UTSG &bull; UTM &bull; UTSC</span>
						</div>
						<h2 class="mt-1 text-base font-bold text-gray-900">Next Competition Announcement Coming Soon</h2>
						<p class="mt-1 text-xs text-gray-600">
							Official club tournaments and campus rounds are scheduled throughout the academic term.
						</p>
					</div>
					<a
						href="/competitions"
						class="inline-flex shrink-0 items-center gap-2 rounded-sm border border-gray-300 bg-white px-4 py-2 text-xs font-medium text-gray-700 transition-colors hover:border-uoft-blue hover:text-uoft-blue"
					>
						Browse All Competitions &rarr;
					</a>
				</div>
			{/if}
		</div>
	</div>
</div>
