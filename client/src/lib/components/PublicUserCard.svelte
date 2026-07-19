<script lang="ts">
import type { User } from "$lib/types";

interface Props {
	user: User;
}

const { user }: Props = $props();
</script>

<a href="/persons/{user.id}" class="group block">
	<div
		class="flex w-full cursor-pointer items-center space-x-4 rounded-xl border border-gray-200 bg-white p-4 text-left shadow-sm transition-all duration-200 hover:border-gray-300 hover:shadow-md"
	>
		<div
			class="flex h-11 w-11 shrink-0 items-center justify-center rounded-full border border-blue-100 bg-blue-50 text-lg font-bold text-blue-600 transition-colors group-hover:bg-blue-100"
		>
			{user.name.charAt(0).toUpperCase()}
		</div>
		<div class="min-w-0 flex-1">
			<p class="truncate text-sm font-bold text-gray-900 transition-colors group-hover:text-blue-600">{user.name}</p>
			<p class="mt-0.5 text-xs font-semibold text-gray-400">{user.student_designator} Competitor</p>
		</div>
		<svg
			class="h-5 w-5 text-gray-400 transition-all group-hover:translate-x-1 group-hover:text-gray-600"
			fill="none"
			stroke="currentColor"
			viewBox="0 0 24 24"
		>
			<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
		</svg>
	</div>
</a>
