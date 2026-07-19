<svelte:head>
	<title>UofT Rubik's Cube Club</title>
	<meta name="description" content="Results, records, and rankings for the University of Toronto Rubik's Cube Club." />
</svelte:head>

<div class="min-h-screen bg-gray-50 px-4 py-12 sm:px-6 lg:px-8">
	<div class="mx-auto max-w-4xl">
		<!-- Hero Section -->
		<div class="py-12 text-center md:py-16">
			<div class="mb-6 inline-flex items-center justify-center rounded-2xl bg-blue-50 p-2">
				<div class="grid h-12 w-12 grid-cols-3 gap-0.5">
					<div class="rounded-sm bg-red-500"></div>
					<div class="rounded-sm bg-blue-600"></div>
					<div class="rounded-sm bg-amber-400"></div>
					<div class="rounded-sm bg-emerald-500"></div>
					<div class="rounded-sm bg-orange-500"></div>
					<div class="rounded-sm border border-gray-200 bg-white"></div>
					<div class="rounded-sm bg-blue-600"></div>
					<div class="rounded-sm bg-red-500"></div>
					<div class="rounded-sm bg-emerald-500"></div>
				</div>
			</div>
			<h1 class="text-4xl font-extrabold tracking-tight text-gray-900 sm:text-5xl">
				UofT <span class="text-blue-600">Rubik's Cube Club</span>
			</h1>
			<p class="mx-auto mt-4 max-w-2xl text-lg text-gray-600">
				The official hub for results, records, and rankings of our club-sanctioned cubing competitions.
			</p>
			<div class="mt-8 flex justify-center gap-4">
				<a
					href="/results"
					class="inline-flex items-center justify-center rounded-xl bg-blue-600 px-5 py-3 text-base font-semibold text-white shadow-sm transition-colors hover:bg-blue-500"
				>
					View Latest Results
				</a>
				<a
					href="/competitions"
					class="inline-flex items-center justify-center rounded-xl border border-gray-200 bg-white px-5 py-3 text-base font-semibold text-gray-700 shadow-sm transition-colors hover:bg-gray-50"
				>
					Competitions
				</a>
			</div>
		</div>

		<!-- Feature Cards Grid -->
		<div class="mt-6 grid gap-6 sm:grid-cols-2">
			<!-- Records Card -->
			<a
				href="/records"
				class="group block rounded-2xl border border-gray-200 bg-white p-6 shadow-sm transition-all duration-200 hover:shadow-md"
			>
				<div class="flex items-center space-x-4">
					<div class="rounded-xl bg-amber-50 p-3 text-amber-600 transition-colors group-hover:bg-amber-100">
						<svg class="h-6 w-6" fill="none" stroke="currentColor" viewBox="0 0 24 24" stroke-width="2">
							<path
								stroke-linecap="round"
								stroke-linejoin="round"
								d="M9 12l2 2 4-4M7.835 4.697a3.42 3.42 0 001.946-.806 3.42 3.42 0 014.438 0 3.42 3.42 0 001.946.806 3.42 3.42 0 013.138 3.138 3.42 3.42 0 00.806 1.946 3.42 3.42 0 010 4.438 3.42 3.42 0 00-.806 1.946 3.42 3.42 0 01-3.138 3.138 3.42 3.42 0 00-1.946.806 3.42 3.42 0 01-4.438 0 3.42 3.42 0 00-1.946-.806 3.42 3.42 0 01-3.138-3.138 3.42 3.42 0 00-.806-1.946 3.42 3.42 0 010-4.438 3.42 3.42 0 00.806-1.946 3.42 3.42 0 013.138-3.138z"
							/>
						</svg>
					</div>
					<div>
						<h3 class="text-lg font-bold text-gray-900 transition-colors group-hover:text-blue-600">Club Records</h3>
						<p class="mt-1 text-sm text-gray-500">Fastest times and historical highlights set at our meetings.</p>
					</div>
				</div>
			</a>

			<!-- Rankings Card -->
			<a
				href="/rankings"
				class="group block rounded-2xl border border-gray-200 bg-white p-6 shadow-sm transition-all duration-200 hover:shadow-md"
			>
				<div class="flex items-center space-x-4">
					<div class="rounded-xl bg-blue-50 p-3 text-blue-600 transition-colors group-hover:bg-blue-100">
						<svg class="h-6 w-6" fill="none" stroke="currentColor" viewBox="0 0 24 24" stroke-width="2">
							<path
								stroke-linecap="round"
								stroke-linejoin="round"
								d="M3 12h.01M3 18h.01M3 6h.01M8 12h13M8 18h13M8 6h13"
							/>
						</svg>
					</div>
					<div>
						<h3 class="text-lg font-bold text-gray-900 transition-colors group-hover:text-blue-600">Rankings</h3>
						<p class="mt-1 text-sm text-gray-500">Compare rankings across different events and formats.</p>
					</div>
				</div>
			</a>

			<!-- Competitors Card -->
			<a
				href="/persons"
				class="group block rounded-2xl border border-gray-200 bg-white p-6 shadow-sm transition-all duration-200 hover:shadow-md"
			>
				<div class="flex items-center space-x-4">
					<div class="rounded-xl bg-emerald-50 p-3 text-emerald-600 transition-colors group-hover:bg-emerald-100">
						<svg class="h-6 w-6" fill="none" stroke="currentColor" viewBox="0 0 24 24" stroke-width="2">
							<path
								stroke-linecap="round"
								stroke-linejoin="round"
								d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z"
							/>
						</svg>
					</div>
					<div>
						<h3 class="text-lg font-bold text-gray-900 transition-colors group-hover:text-blue-600">Competitors</h3>
						<p class="mt-1 text-sm text-gray-500">Look up member profiles, personal records, and solve history.</p>
					</div>
				</div>
			</a>

			<!-- Admin Dashboard Card -->
			<a
				href="/dashboard"
				class="group block rounded-2xl border border-gray-200 bg-white p-6 shadow-sm transition-all duration-200 hover:shadow-md"
			>
				<div class="flex items-center space-x-4">
					<div class="rounded-xl bg-purple-50 p-3 text-purple-600 transition-colors group-hover:bg-purple-100">
						<svg class="h-6 w-6" fill="none" stroke="currentColor" viewBox="0 0 24 24" stroke-width="2">
							<path
								stroke-linecap="round"
								stroke-linejoin="round"
								d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z"
							/>
							<path stroke-linecap="round" stroke-linejoin="round" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
						</svg>
					</div>
					<div>
						<h3 class="text-lg font-bold text-gray-900 transition-colors group-hover:text-blue-600">Admin Area</h3>
						<p class="mt-1 text-sm text-gray-500">Manage competition records, academic sessions, and users.</p>
					</div>
				</div>
			</a>
		</div>
	</div>
</div>
