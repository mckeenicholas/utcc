<script lang="ts">
	import { goto } from '$app/navigation';
	import { onMount } from 'svelte';
	import { BASE_URL, checkLoginStatus } from '$lib/utils';
	import type { Competition, Paginated } from '$lib/types';
	import authFetch from '$lib/authFetch';
	import { DatePicker } from 'bits-ui';
	import { type DateValue } from '@internationalized/date';
	import LoadingScreen from '$lib/components/LoadingScreen.svelte';

	const PAGINATION_SIZE = 20;

	let competitions: Competition[] = $state([]);
	let loading = $state(true);
	let newCompName = $state('');
	let selectedDate = $state<DateValue | undefined>(undefined);
	let currentPage = $state(1);
	let totalPages = $state(1);
	let hasNext = $state(false);
	let hasPrevious = $state(false);
	let totalCount = $state(0);

	const fetchCompetitions = async (page: number = 1) => {
		const competitionRes = await authFetch(`${BASE_URL}/api/competitions/?page=${page}`);

		if (competitionRes.ok) {
			const compResJSON: Paginated<Competition> = await competitionRes.json();
			competitions = compResJSON.results.sort(
				(a, b) => new Date(b.date).getTime() - new Date(a.date).getTime()
			);

			// Update pagination state
			currentPage = page;
			totalCount = compResJSON.count;
			hasNext = !!compResJSON.next;
			hasPrevious = !!compResJSON.previous;
			totalPages = Math.ceil(totalCount / PAGINATION_SIZE);

			loading = false;
		} else if (competitionRes.status === 401) {
			goto('/dashboard/signin');
		}
	};

	onMount(async () => {
		const loggedIn = await checkLoginStatus();

		if (!loggedIn) {
			goto('/dashboard/signin');
			return;
		}

		await fetchCompetitions(1);
	});

	const goToNextPage = () => {
		if (hasNext) {
			fetchCompetitions(currentPage + 1);
		}
	};

	const goToPreviousPage = () => {
		if (hasPrevious) {
			fetchCompetitions(currentPage - 1);
		}
	};

	const deleteCompetition = async (id: number) => {
		if (confirm('Are you sure you want to delete this competition?')) {
			const response = await authFetch(`${BASE_URL}/api/competitions/${id}/`, {
				method: 'DELETE',
				headers: {
					'Content-Type': 'application/json'
				}
			});

			if (response.ok) {
				competitions = competitions.filter((c) => c.id !== id);
			} else {
				alert('Failed to delete competition');
			}
		}
	};

	const createCompetition = async () => {
		if (!selectedDate) {
			alert('Please select a date');
			return;
		}

		const dateString = selectedDate.toString();

		const response = await authFetch(`${BASE_URL}/api/competitions/`, {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json'
			},
			body: JSON.stringify({ name: newCompName, date: dateString })
		});

		if (response.ok) {
			const newCompetition: Competition = await response.json();
			// Reset form
			newCompName = '';
			selectedDate = undefined;
			// Navigate directly to the new competition
			goto(`/dashboard/competitions/${newCompetition.id}`);
		} else {
			alert('Failed to create competition');
		}
	};
</script>

{#if loading}
	<LoadingScreen message="Loading Dashboard" />
{:else}
	<div class="min-h-screen py-8">
		<div class="mx-auto max-w-4xl px-4">
			<!-- Header -->
			<div class="mb-8 flex items-center justify-between">
				<h1 class="text-3xl font-bold text-gray-900">UofT Rubik's Cube Club Dashboard</h1>
				<a
					href="/dashboard/signout"
					class="rounded-md bg-gray-600 px-4 py-2 text-white hover:bg-gray-700 focus:outline-none focus:ring-2 focus:ring-gray-500 focus:ring-offset-2"
				>
					Sign Out
				</a>
			</div>

			<!-- Add New Competition Section -->
			<div class="rounded-lg bg-white p-6 shadow-sm">
				<h2 class="mb-4 text-xl font-semibold text-gray-800">Add New Competition</h2>
				<div class="space-y-4">
					<div>
						<label for="new-comp-name" class="block text-sm font-medium text-gray-700"
							>Competition Name</label
						>
						<input
							id="new-comp-name"
							placeholder="Enter competition name"
							bind:value={newCompName}
							class="mt-1 block w-full rounded-md border border-gray-300 px-3 py-2 shadow-sm focus:border-gray-500 focus:outline-none focus:ring-1 focus:ring-gray-500"
						/>
					</div>
					<div>
						<DatePicker.Root bind:value={selectedDate} weekdayFormat="short" fixedWeeks={true}>
							<div class="flex w-full flex-col gap-1.5">
								<DatePicker.Label class="block text-sm font-medium text-gray-700">
									Competition Date
								</DatePicker.Label>
								<DatePicker.Input
									class="flex w-full items-center rounded-md border border-gray-300 px-3 py-1 text-sm shadow-sm focus-within:border-gray-500 focus-within:ring-1 focus-within:ring-gray-500 hover:border-gray-400"
								>
									{#snippet children({ segments })}
										{#each segments as { part, value }, i (part + i)}
											<div class="-m-0.5 inline-block select-none">
												{#if part === 'literal'}
													<DatePicker.Segment {part} class="px-1 text-gray-500">
														{value}
													</DatePicker.Segment>
												{:else}
													<DatePicker.Segment
														{part}
														class="rounded px-1 py-1 hover:bg-gray-100 focus:bg-gray-100 focus:text-gray-900 focus-visible:ring-0 focus-visible:ring-offset-0 aria-[valuetext=Empty]:text-gray-400"
													>
														{value}
													</DatePicker.Segment>
												{/if}
											</div>
										{/each}
										<DatePicker.Trigger
											class="ml-auto inline-flex h-8 w-8 items-center justify-center rounded text-gray-600 transition-colors hover:bg-gray-100 hover:text-gray-800"
										>
											<svg class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
												<path
													stroke-linecap="round"
													stroke-linejoin="round"
													stroke-width="2"
													d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"
												/>
											</svg>
										</DatePicker.Trigger>
									{/snippet}
								</DatePicker.Input>
								<DatePicker.Content sideOffset={6} class="z-50">
									<DatePicker.Calendar
										class="rounded-lg border border-gray-200 bg-white p-4 shadow-lg"
									>
										{#snippet children({ months, weekdays })}
											<DatePicker.Header class="mb-4 flex items-center justify-between">
												<DatePicker.PrevButton
													class="inline-flex h-9 w-9 items-center justify-center rounded-md transition-colors hover:bg-gray-100"
												>
													<svg
														class="h-4 w-4"
														fill="none"
														stroke="currentColor"
														viewBox="0 0 24 24"
													>
														<path
															stroke-linecap="round"
															stroke-linejoin="round"
															stroke-width="2"
															d="M15 19l-7-7 7-7"
														/>
													</svg>
												</DatePicker.PrevButton>
												<DatePicker.Heading class="text-sm font-medium" />
												<DatePicker.NextButton
													class="inline-flex h-9 w-9 items-center justify-center rounded-md transition-colors hover:bg-gray-100"
												>
													<svg
														class="h-4 w-4"
														fill="none"
														stroke="currentColor"
														viewBox="0 0 24 24"
													>
														<path
															stroke-linecap="round"
															stroke-linejoin="round"
															stroke-width="2"
															d="M9 5l7 7-7 7"
														/>
													</svg>
												</DatePicker.NextButton>
											</DatePicker.Header>
											<div class="flex flex-col space-y-4">
												{#each months as month (month.value)}
													<DatePicker.Grid class="w-full border-collapse space-y-1">
														<DatePicker.GridHead>
															<DatePicker.GridRow class="mb-1 flex w-full justify-between">
																{#each weekdays as day (day)}
																	<DatePicker.HeadCell
																		class="w-9 rounded-md text-xs font-normal text-gray-500"
																	>
																		<div>{day.slice(0, 2)}</div>
																	</DatePicker.HeadCell>
																{/each}
															</DatePicker.GridRow>
														</DatePicker.GridHead>
														<DatePicker.GridBody>
															{#each month.weeks as weekDates (weekDates)}
																<DatePicker.GridRow class="flex w-full">
																	{#each weekDates as date (date)}
																		<DatePicker.Cell
																			{date}
																			month={month.value}
																			class="relative h-9 w-9 p-0 text-center text-sm"
																		>
																			<DatePicker.Day
																				class="data-selected:bg-gray-900 data-selected:text-white data-disabled:text-gray-300 data-disabled:pointer-events-none data-outside-month:pointer-events-none data-outside-month:text-gray-400 data-unavailable:text-gray-300 data-unavailable:line-through inline-flex h-9 w-9 items-center justify-center whitespace-nowrap rounded-md text-sm font-normal text-gray-900 transition-colors hover:bg-gray-100"
																			>
																				{date.day}
																			</DatePicker.Day>
																		</DatePicker.Cell>
																	{/each}
																</DatePicker.GridRow>
															{/each}
														</DatePicker.GridBody>
													</DatePicker.Grid>
												{/each}
											</div>
										{/snippet}
									</DatePicker.Calendar>
								</DatePicker.Content>
							</div>
						</DatePicker.Root>
					</div>
					<button
						onclick={createCompetition}
						disabled={!newCompName || !selectedDate}
						class="w-full rounded-md bg-green-600 px-4 py-2 text-white hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-green-500 focus:ring-offset-2 disabled:cursor-not-allowed disabled:bg-gray-400"
					>
						Create Competition
					</button>
				</div>
			</div>

			<!-- Competitions Section -->
			<div class="mb-8 mt-4">
				<h2 class="mb-4 ms-2 text-2xl font-semibold text-gray-800">Competitions</h2>

				{#if competitions.length === 0}
					<div class="rounded-lg bg-white p-6 shadow-sm">
						<p class="text-center text-gray-500">No competitions added yet</p>
					</div>
				{:else}
					<div class="grid gap-4">
						{#each competitions as competition (competition.id)}
							<div class="rounded-lg bg-white p-4 shadow-sm transition-shadow hover:shadow-md">
								<div class="flex items-center justify-between">
									<div>
										<h3 class="font-medium text-gray-900">{competition.name}</h3>
										<p class="text-sm text-gray-500">
											{new Date(competition.date).toLocaleDateString()}
										</p>
									</div>
									<div class="flex space-x-2">
										<a
											href={`/dashboard/competitions/${competition.id}`}
											class="rounded-md bg-blue-100 px-3 py-1 text-sm text-blue-800 hover:bg-blue-200"
										>
											View
										</a>
										<button
											onclick={() => goto(`/dashboard/competitions/${competition.id}/edit`)}
											class="rounded-md bg-yellow-100 px-3 py-1 text-sm text-yellow-800 hover:bg-yellow-200"
										>
											Edit Info
										</button>
										<button
											onclick={() => deleteCompetition(competition.id)}
											class="rounded-md bg-red-100 px-3 py-1 text-sm text-red-800 hover:bg-red-200"
										>
											Delete
										</button>
									</div>
								</div>
							</div>
						{/each}
					</div>

					<!-- Pagination Controls -->
					{#if totalPages > 1}
						<div class="mt-6 flex items-center justify-between rounded-lg bg-white p-4 shadow-sm">
							<div class="text-sm text-gray-500">
								Showing page {currentPage} of {totalPages} ({totalCount} total competitions)
							</div>
							<div class="flex space-x-2">
								<button
									onclick={goToPreviousPage}
									disabled={!hasPrevious}
									class="disabled: inline-flex items-center rounded-md bg-gray-100 px-3 py-2 text-sm font-medium text-gray-700 hover:bg-gray-200 focus:outline-none focus:ring-2 focus:ring-gray-500 focus:ring-offset-2 disabled:cursor-not-allowed disabled:text-gray-400"
								>
									<svg class="mr-1 h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
										<path
											stroke-linecap="round"
											stroke-linejoin="round"
											stroke-width="2"
											d="M15 19l-7-7 7-7"
										/>
									</svg>
									Previous
								</button>
								<button
									onclick={goToNextPage}
									disabled={!hasNext}
									class="disabled: inline-flex items-center rounded-md bg-gray-100 px-3 py-2 text-sm font-medium text-gray-700 hover:bg-gray-200 focus:outline-none focus:ring-2 focus:ring-gray-500 focus:ring-offset-2 disabled:cursor-not-allowed disabled:text-gray-400"
								>
									Next
									<svg class="ml-1 h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
										<path
											stroke-linecap="round"
											stroke-linejoin="round"
											stroke-width="2"
											d="M9 5l7 7-7 7"
										/>
									</svg>
								</button>
							</div>
						</div>
					{/if}
				{/if}
			</div>
		</div>
	</div>
{/if}
