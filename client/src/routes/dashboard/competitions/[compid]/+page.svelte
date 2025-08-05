<script lang="ts">
	import { onMount } from 'svelte';
	import { page } from '$app/stores';
	import type { Competition, CompetitionResults, Result, WCAEvent, User } from '$lib/types';
	import { BASE_URL } from '$lib/utils';
	import authFetch from '$lib/authFetch';
	import ResultForm from '$lib/components/ResultForm.svelte';
	import ResultsTable from '$lib/components/ResultsTable.svelte';
	import PageHeader from '$lib/components/PageHeader.svelte';
	import ErrorMessage from '$lib/components/ErrorMessage.svelte';
	import LoadingScreen from '$lib/components/LoadingScreen.svelte';

	const compId = $page.params.compid;

	let competition: Competition | null = $state(null);
	let results: Result[] = $state([]);
	let loading = $state(true);
	let submitting = $state(false);
	let errorMessage = $state<string | null>(null);
	let editingResult: Result | null = $state(null);

	// User search and autocomplete state
	let userSearchTerm = $state('');
	let userSearchResults: User[] = $state([]);
	let userSearchLoading = $state(false);
	let userSearchTimeout: number | null = null;
	let selectedUserId: number | null = $state(null);
	let selectedUserName = $state('');
	let showCreateUserModal = $state(false);
	let newUserName = $state('');
	let creatingUser = $state(false);
	let selectedDropdownIndex = $state(-1);

	let showUserDropdown = $derived(selectedUserId == null && userSearchTerm !== '');

	// Form state
	let formData = $state({
		name: '',
		event: '333' as WCAEvent,
		round: 1,
		time1: 0,
		time2: 0,
		time3: 0,
		time4: 0,
		time5: 0
	});

	// Track the selected person_id separately
	let selectedPersonId: number | null = $state(null);

	$effect(() => {
		if (!selectedPersonId) {
			resetFormTimes();
			editingResult = null;
			return;
		}

		const existingResult = results.find(
			(result) =>
				result.person_id === selectedPersonId &&
				result.event === formData.event &&
				result.round === formData.round
		);

		if (existingResult) {
			// Pre-populate the form with the found result's times
			formData.time1 = existingResult.time1;
			formData.time2 = existingResult.time2;
			formData.time3 = existingResult.time3;
			formData.time4 = existingResult.time4;
			formData.time5 = existingResult.time5;
			editingResult = existingResult;
		} else {
			// If no matching result is found for the new combination, reset the times
			// but keep the user/event/round selected.
			resetFormTimes();
			editingResult = null;
		}
	});

	const fetchData = async () => {
		try {
			// Fetch competition details
			const compResponse = await fetch(`${BASE_URL}/api/competitions/${compId}/`);
			if (!compResponse.ok) throw new Error('Failed to fetch competition');
			competition = await compResponse.json();

			// Fetch results for this competition
			const resultsResponse = await fetch(`${BASE_URL}/api/competitions/${compId}/results/`);
			if (!resultsResponse.ok) throw new Error('Failed to fetch results');
			const resultsData: CompetitionResults = await resultsResponse.json();

			// Flatten the results from the nested structure
			results = (resultsData.results || []).flatMap((eventResult) =>
				eventResult.rounds.flatMap((round) =>
					round.results.map((person) => ({
						id: person.id,
						person_name: person.person_name,
						person_id: person.person_id,
						competition: Number(compId),
						event: eventResult.event,
						round: round.round,
						time1: person.times[0] || 0,
						time2: person.times[1] || 0,
						time3: person.times[2] || 0,
						time4: person.times[3] || 0,
						time5: person.times[4] || 0,
						single: person.single,
						average: person.average
					}))
				)
			);
		} catch (error) {
			errorMessage = error instanceof Error ? error.message : 'An error occurred';
			console.error(error);
		} finally {
			loading = false;
		}
	};

	// User search functions
	const searchUsers = async (query: string) => {
		if (!query.trim()) {
			userSearchResults = [];
			userSearchLoading = false;
			selectedDropdownIndex = -1;
			return;
		}

		userSearchLoading = true;
		try {
			const response = await fetch(
				`${BASE_URL}/api/users/persons/search/?name=${encodeURIComponent(query)}`
			);
			const data = await response.json();
			userSearchResults = data.results || data || [];
			selectedDropdownIndex = -1; // Reset selection when new results come in
		} catch (error) {
			console.error('User search failed:', error);
			userSearchResults = [];
			selectedDropdownIndex = -1;
		} finally {
			userSearchLoading = false;
		}
	};

	const debouncedUserSearch = (query: string) => {
		if (userSearchTimeout) {
			clearTimeout(userSearchTimeout);
		}

		userSearchTimeout = setTimeout(() => {
			searchUsers(query);
		}, 300);
	};

	// Keyboard navigation functions
	const handleKeyboardNavigation = (event: KeyboardEvent) => {
		if (!showUserDropdown || userSearchResults.length === 0) return;

		const totalItems = userSearchResults.length + (userSearchTerm.trim() ? 1 : 0); // +1 for "Add user" option

		switch (event.key) {
			case 'ArrowDown':
				event.preventDefault();
				selectedDropdownIndex = (selectedDropdownIndex + 1) % totalItems;
				break;
			case 'ArrowUp':
				event.preventDefault();
				selectedDropdownIndex =
					selectedDropdownIndex <= 0 ? totalItems - 1 : selectedDropdownIndex - 1;
				break;
			case 'Enter':
				event.preventDefault();
				if (selectedDropdownIndex >= 0) {
					if (selectedDropdownIndex < userSearchResults.length) {
						// Select a user
						selectUser(userSearchResults[selectedDropdownIndex]);
					} else {
						// Select "Add user" option
						showCreateUserModal = true;
					}
				}
				break;
			case 'Escape':
				event.preventDefault();
				selectedDropdownIndex = -1;
				userSearchTerm = '';
				break;
		}
	};

	// Reactive effect for user search
	$effect(() => {
		debouncedUserSearch(userSearchTerm);
	});

	const selectUser = (user: User) => {
		selectedUserId = user.id;
		selectedUserName = user.name;
		userSearchTerm = user.name;
		selectedPersonId = user.id;
		formData.name = user.name;
		selectedDropdownIndex = -1;
	};

	const clearUserSelection = () => {
		selectedUserId = null;
		selectedUserName = '';
		userSearchTerm = '';
		selectedPersonId = null; // This will trigger the main $effect to clear the form
		formData.name = '';
		selectedDropdownIndex = -1;
	};

	const resetFormTimes = () => {
		formData.time1 = 0;
		formData.time2 = 0;
		formData.time3 = 0;
		formData.time4 = 0;
		formData.time5 = 0;
	};

	const createNewUser = async () => {
		if (!newUserName.trim()) return;

		creatingUser = true;
		try {
			const response = await authFetch(`${BASE_URL}/api/users/persons/`, {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json'
				},
				body: JSON.stringify({ name: newUserName })
			});

			if (response.ok) {
				const newUser = await response.json();
				selectUser(newUser);
				showCreateUserModal = false;
				newUserName = '';
			}
		} catch (error) {
			console.error('Failed to create user:', error);
		} finally {
			creatingUser = false;
		}
	};

	const submitResult = async () => {
		if (!selectedPersonId) {
			errorMessage = 'Please select a user';
			return;
		}

		submitting = true;
		errorMessage = null;

		try {
			const url = editingResult
				? `${BASE_URL}/api/results/${editingResult.id}/`
				: `${BASE_URL}/api/results/`;

			const method = editingResult ? 'PUT' : 'POST';

			const response = await authFetch(url, {
				method,
				headers: {
					'Content-Type': 'application/json'
				},
				body: JSON.stringify({
					...formData,
					person_id: selectedPersonId,
					competition: Number(compId)
				})
			});

			if (!response.ok) {
				const errorData = await response.json().catch(() => ({
					message: editingResult ? 'Failed to update result' : 'Failed to submit result'
				}));
				throw new Error(
					errorData.message ||
						(editingResult ? 'Failed to update result' : 'Failed to submit result')
				);
			}

			// Reset form and editing state
			resetForm();

			// Refresh results
			await fetchData();
		} catch (error) {
			errorMessage =
				error instanceof Error
					? error.message
					: editingResult
						? 'Failed to update result'
						: 'Failed to submit result';
			console.error(error);
		} finally {
			submitting = false;
		}
	};

	const resetForm = () => {
		formData = {
			name: '',
			event: '333' as WCAEvent,
			round: 1,
			time1: 0,
			time2: 0,
			time3: 0,
			time4: 0,
			time5: 0
		};
		editingResult = null;
		clearUserSelection();
	};

	const editResult = (result: Result) => {
		editingResult = result;
		formData = {
			name: result.person_name,
			event: result.event,
			round: result.round,
			time1: result.time1,
			time2: result.time2,
			time3: result.time3,
			time4: result.time4,
			time5: result.time5
		};

		// Set the user selection
		selectedUserId = result.person_id;
		selectedUserName = result.person_name;
		userSearchTerm = result.person_name;
		selectedPersonId = result.person_id;

		// Scroll to form
		document.querySelector('.submit-form')?.scrollIntoView({ behavior: 'smooth' });
	};

	const cancelEdit = () => {
		resetForm();
	};

	const deleteResult = async (resultId: number) => {
		if (!confirm('Are you sure you want to delete this result?')) return;

		try {
			const response = await authFetch(`${BASE_URL}/api/results/${resultId}/`, {
				method: 'DELETE'
			});

			if (!response.ok) {
				throw new Error('Failed to delete result');
			}

			await fetchData();
		} catch (error) {
			errorMessage = error instanceof Error ? error.message : 'Failed to delete result';
			console.error(error);
		}
	};

	onMount(fetchData);
</script>

{#if loading}
	<LoadingScreen message="Loading Competition" />
{:else}
	<div class="min-h-screen py-8">
		<div class="mx-auto max-w-[1500px] px-4">
			<!-- Header with Navigation -->
			<PageHeader {competition} />

			<!-- Error Message -->
			<ErrorMessage message={errorMessage} />

			<!-- Main Content Layout: Form on Left, Results on Right (Desktop) / Stacked (Mobile) -->
			<div class="grid grid-cols-1 gap-8 lg:grid-cols-4">
				<!-- Submit Result Form -->
				<div class="lg:col-span-1">
					<div class="rounded-lg bg-white p-6 shadow-sm">
						{#if !editingResult}
							<h3 class="mb-4 text-lg font-semibold text-gray-800">Select User</h3>

							<div class="relative">
								<label for="user-search" class="mb-1 block text-sm font-medium text-gray-700">
									Person
								</label>
								<input
									id="user-search"
									type="text"
									placeholder="Type to search users..."
									bind:value={userSearchTerm}
									onfocus={() => {
										if (userSearchTerm.length > 0) selectedDropdownIndex = -1;
									}}
									onblur={() => setTimeout(() => (selectedDropdownIndex = -1), 200)}
									onkeydown={handleKeyboardNavigation}
									class="w-full rounded-md border border-gray-300 px-3 py-2 shadow-sm focus:border-gray-500 focus:outline-none focus:ring-1 focus:ring-gray-500"
									autocomplete="off"
								/>

								<!-- User selected indicator -->
								{#if selectedUserId && selectedUserName}
									<div
										class="mt-2 flex items-center justify-between rounded-md border border-green-200 bg-green-50 px-3 py-2"
									>
										<div class="flex items-center space-x-2">
											<div
												class="flex h-6 w-6 items-center justify-center rounded-full bg-green-100 text-xs font-medium text-green-800"
											>
												{selectedUserName.charAt(0).toUpperCase()}
											</div>
											<span class="text-sm text-green-800">{selectedUserName}</span>
										</div>

										<button
											type="button"
											onclick={clearUserSelection}
											aria-label="Clear user selection"
											class="text-green-600 hover:text-green-800"
										>
											<svg class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
												<path
													stroke-linecap="round"
													stroke-linejoin="round"
													stroke-width="2"
													d="M6 18L18 6M6 6l12 12"
												/>
											</svg>
										</button>
									</div>
								{/if}

								<!-- Dropdown with search results -->
								{#if showUserDropdown}
									<div
										class="absolute z-10 mt-1 max-h-60 w-full overflow-y-auto rounded-md border border-gray-300 bg-white shadow-lg"
									>
										{#if userSearchLoading}
											<div class="flex items-center px-3 py-2 text-sm text-gray-500">
												<div
													class="mr-2 h-4 w-4 animate-spin rounded-full border-2 border-gray-300 border-t-gray-600"
												></div>
												Searching...
											</div>
										{:else if userSearchResults.length > 0}
											{#each userSearchResults as user, index (user.id)}
												<button
													type="button"
													onclick={() => selectUser(user)}
													class="flex w-full items-center space-x-2 border-b border-gray-100 px-3 py-2 text-left last:border-b-0 hover:bg-gray-100 {selectedDropdownIndex ===
													index
														? 'bg-blue-100'
														: ''}"
												>
													<div
														class="flex h-6 w-6 items-center justify-center rounded-full bg-blue-100 text-xs font-medium text-blue-800"
													>
														{user.name.charAt(0).toUpperCase()}
													</div>
													<span class="text-sm">{user.name}</span>
													<span class="text-xs text-gray-500">ID: {user.id}</span>
												</button>
											{/each}
										{:else if userSearchTerm.trim()}
											<div class="px-3 py-2 text-sm text-gray-500">No users found</div>
										{/if}

										<!-- Add user option -->
										{#if userSearchTerm.trim()}
											<button
												type="button"
												onclick={() => (showCreateUserModal = true)}
												class="flex w-full items-center space-x-2 border-t border-gray-200 px-3 py-2 text-left text-green-700 hover:bg-green-50 {selectedDropdownIndex ===
												userSearchResults.length
													? 'bg-green-100'
													: ''}"
											>
												<svg class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
													<path
														stroke-linecap="round"
														stroke-linejoin="round"
														stroke-width="2"
														d="M12 6v6m0 0v6m0-6h6m-6 0H6"
													/>
												</svg>
												<span class="text-sm">Add new user: "{userSearchTerm}"</span>
											</button>
										{/if}
									</div>
								{/if}
							</div>
						{/if}

						{#if editingResult}
							<div class="mb-2 rounded-md border border-blue-200 bg-blue-50 p-3">
								<p class="text-sm text-blue-800">
									Editing: <span class="font-medium">{editingResult.person_name}</span> -
									{editingResult.event} Round {editingResult.round}
								</p>
							</div>
						{/if}

						<div class="mb-2 flex items-center justify-between">
							{#if editingResult}
								<button
									onclick={cancelEdit}
									class="mt-1 rounded-md bg-gray-200 px-2 py-1 text-sm text-gray-700 hover:bg-gray-300 hover:text-gray-700"
								>
									Cancel
								</button>
							{/if}
						</div>

						<ResultForm
							{formData}
							{editingResult}
							{submitting}
							additionalValidation={!!selectedPersonId}
							onSubmit={() => {
								if (!selectedPersonId) {
									errorMessage = 'Please select a user';
									return;
								}
								submitResult();
							}}
							onCancel={cancelEdit}
						/>
					</div>
				</div>

				<!-- Results Table -->
				<div class="lg:col-span-3">
					<ResultsTable {results} onEdit={editResult} onDelete={deleteResult} />
				</div>
			</div>
		</div>
	</div>

	<!-- Create User Modal -->
	{#if showCreateUserModal}
		<div class="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-50">
			<div class="mx-4 w-full max-w-md rounded-lg bg-white p-6 shadow-xl">
				<h3 class="mb-4 text-lg font-semibold text-gray-900">Add New User</h3>
				<div class="space-y-4">
					<div>
						<label for="new-user-name" class="mb-1 block text-sm font-medium text-gray-700">
							User Name
						</label>
						<input
							id="new-user-name"
							type="text"
							bind:value={newUserName}
							placeholder="Enter user name"
							class="w-full rounded-md border border-gray-300 px-3 py-2 shadow-sm focus:border-gray-500 focus:outline-none focus:ring-1 focus:ring-gray-500"
						/>
					</div>
					<div class="flex space-x-3">
						<button
							onclick={createNewUser}
							disabled={creatingUser || !newUserName.trim()}
							class="flex-1 rounded-md bg-green-600 px-4 py-2 text-white hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-green-500 focus:ring-offset-2 disabled:cursor-not-allowed disabled:bg-gray-400"
						>
							{creatingUser ? 'Creating...' : 'Create User'}
						</button>
						<button
							onclick={() => {
								showCreateUserModal = false;
								newUserName = '';
							}}
							class="rounded-md bg-gray-300 px-4 py-2 text-gray-700 hover:bg-gray-400 focus:outline-none focus:ring-2 focus:ring-gray-500 focus:ring-offset-2"
						>
							Cancel
						</button>
					</div>
				</div>
			</div>
		</div>
	{/if}
{/if}
