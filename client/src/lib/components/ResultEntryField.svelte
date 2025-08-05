<script lang="ts">
	// Props with bindable value that can be a function tuple [getter, setter] or number
	let { value = $bindable(0), placeholder = 'Enter time', id, disabled = false } = $props();

	const DNF_KEYS = ['d', 'D', '/', '#'];
	const DNS_KEYS = ['s', 'S', '*'];

	let displayValue = $state('');

	// Helper to get/set value (supports both direct values and custom binding tuples)
	const getValue = () => {
		if (Array.isArray(value) && typeof value[0] === 'function') {
			return value[0]();
		}
		return value;
	};

	const setValue = (newValue: number) => {
		if (Array.isArray(value) && typeof value[1] === 'function') {
			value[1](newValue);
		} else {
			value = newValue;
		}
	};

	$effect(() => {
		const currentValue = getValue();
		if (currentValue === 0) {
			displayValue = '';
		} else {
			displayValue = toClockFormat(currentValue);
		}
	});

	const toInt = (input: string): number | null => {
		const int = parseInt(input);
		return isNaN(int) ? null : int;
	};

	const toCentiseconds = (input: string): number => {
		if (input === '') return 0;
		if (input === 'DNF') return -1;
		if (input === 'DNS') return -2;
		const num = toInt(input.replace(/\D/g, '')) || 0;
		return (
			Math.floor(num / 1000000) * 360000 +
			Math.floor((num % 1000000) / 10000) * 6000 +
			Math.floor((num % 10000) / 100) * 100 +
			(num % 100)
		);
	};

	const toClockFormat = (centiseconds: number): string => {
		if (centiseconds === -1) return 'DNF';
		if (centiseconds === -2) return 'DNS';
		if (centiseconds == null || !Number.isFinite(centiseconds) || centiseconds < 0) {
			return '';
		}
		return new Date(centiseconds * 10)
			.toISOString()
			.substr(11, 11)
			.replace(/^[0:]*(?!\.)/g, '');
	};

	const reformatInput = (input: string): string => {
		const number = toInt(input.replace(/\D/g, '')) || 0;
		if (number === 0) return '';
		const str = '00000000' + number.toString().slice(0, 8);
		const match = str.match(/(\d\d)(\d\d)(\d\d)(\d\d)$/);
		if (!match) return '';
		const [, hh, mm, ss, cc] = match;
		return `${hh}:${mm}:${ss}.${cc}`.replace(/^[0:]*(?!\.)/g, '');
	};

	const handleInput = (event: Event) => {
		const input = event.target as HTMLInputElement;
		const inputValue = input.value;
		const key = inputValue.slice(-1);

		if (inputValue.trim() === '') {
			displayValue = '';
			setValue(0);
		} else if (DNF_KEYS.includes(key)) {
			displayValue = 'DNF';
			setValue(-1);
		} else if (DNS_KEYS.includes(key)) {
			displayValue = 'DNS';
			setValue(-2);
		} else {
			displayValue = reformatInput(inputValue);
			setValue(toCentiseconds(displayValue));
		}
	};

	const handleKeydown = (event: KeyboardEvent) => {
		if (event.key === 'Enter' || event.key === 'ArrowDown' || event.key === '+') {
			event.preventDefault();
			const inputs = document.querySelectorAll('.time-input');
			const currentIndex = Array.from(inputs).indexOf(event.target as HTMLInputElement);
			const nextInput = inputs[currentIndex + 1] as HTMLInputElement;
			if (nextInput) {
				nextInput.focus();
			} else {
				const submitButton = document.querySelector('.submit-button') as HTMLButtonElement;
				if (submitButton) {
					submitButton.focus();
				}
			}
		} else if (event.key === 'ArrowUp' || event.key === '-') {
			event.preventDefault();
			const inputs = document.querySelectorAll('.time-input');
			const currentIndex = Array.from(inputs).indexOf(event.target as HTMLInputElement);
			const prevInput = inputs[currentIndex - 1] as HTMLInputElement;
			if (prevInput) {
				prevInput.focus();
			}
		}
	};
</script>

<input
	{id}
	{disabled}
	class="time-input block w-full rounded-md border border-gray-300 px-3 py-2 shadow-sm focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500 disabled:cursor-not-allowed disabled:bg-gray-100 disabled:text-gray-500"
	type="text"
	bind:value={displayValue}
	oninput={handleInput}
	onkeydown={handleKeydown}
	{placeholder}
/>
