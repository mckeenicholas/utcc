<script lang="ts">
const currentYear = new Date().getFullYear();
</script>

<footer class="mt-auto border-t border-gray-200 bg-white">
	<div class="mx-auto max-w-6xl px-4 py-12 sm:px-6 lg:py-10">
		<div class="grid grid-cols-1 gap-8 sm:grid-cols-2 sm:gap-10 lg:grid-cols-4">
			<!-- Col 1: Brand & Identity -->
			<div class="flex flex-col gap-4">
				<a href="/" class="flex items-center gap-2.5">
					<img
						src="/client-static/logo.png"
						alt="University of Toronto Cube Club Logo"
						class="h-8 w-8 rounded-full object-contain"
					/>
					<span class="text-base font-bold tracking-tight text-uoft-blue"> U of T Cube Club </span>
				</a>
			</div>

			<div class="flex flex-col gap-2.5 sm:contents">
				<div>
					<ul class="flex flex-col gap-2.5 sm:mt-4">
						<li>
							<a href="/results" class="text-xs text-gray-600 transition-colors hover:text-uoft-blue">
								Official Results
							</a>
						</li>
						<li>
							<a href="/records" class="text-xs text-gray-600 transition-colors hover:text-uoft-blue"> Club Records </a>
						</li>
					</ul>
				</div>

				<div>
					<ul class="flex flex-col gap-2.5 sm:mt-4">
						<li>
							<a href="/rankings" class="text-xs text-gray-600 transition-colors hover:text-uoft-blue"> Rankings </a>
						</li>
						<li>
							<a href="/competitions" class="text-xs text-gray-600 transition-colors hover:text-uoft-blue">
								Competitions
							</a>
						</li>
					</ul>
				</div>

				<div>
					<ul class="flex flex-col gap-2.5 sm:mt-4">
						<li>
							<a href="/persons" class="text-xs text-gray-600 transition-colors hover:text-uoft-blue"> Competitors </a>
						</li>
						<li>
							<a href="/dashboard/signin" class="text-xs text-gray-600 transition-colors hover:text-uoft-blue">
								Sign In
							</a>
						</li>
					</ul>
				</div>
			</div>
		</div>

		<!-- Bottom Copyright & Academic Disclaimers -->
		<div
			class="mt-12 flex flex-col items-start justify-between gap-4 border-t border-gray-100 pt-8 sm:flex-row sm:items-center"
		>
			<p class="text-xs text-gray-700">
				&copy; {currentYear} University of Toronto Cube Club.
			</p>
			<p class="text-[11px] text-gray-400">UTSG &bull; UTM &bull; UTSC</p>
		</div>
	</div>
</footer>
