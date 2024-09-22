#include <coroutine>
#include <iostream>

template<typename T>
class Generator {
public:
    struct promise_type;
    using handle_type = std::coroutine_handle<promise_type>;

    struct promise_type {
        T value;

        auto get_return_object() {
            return Generator{ handle_type::from_promise(*this) };
        }

        auto initial_suspend() {
            return std::suspend_always{};
        }

        auto final_suspend() noexcept {
            return std::suspend_always{};
        }

        auto yield_value(T v) {
            value = v;
            return std::suspend_always{};
        }

        void return_void() {
        }

        void unhandled_exception() {
            std::terminate();
        }
    };

    handle_type coro;

    Generator(handle_type h) : coro(h) {
    }

    ~Generator() {
        if (coro && coro.done()) {
            coro.destroy();
            coro = nullptr;
        }
    }


    bool done() const {
        return coro.done();
    }

    T next() {
        coro.resume();
        return coro.promise().value;
    }

    struct iterator {
        handle_type coro;
        bool done;

        iterator(handle_type h) : coro(h), done(!h || h.done()) {
        }

        bool operator!=(std::default_sentinel_t) const {
            return !done;
        }

        iterator& operator++() {
            coro.resume();
            done = coro.done();
            return *this;
        }

        T operator*() const {
            return coro.promise().value;
        }
    };

    iterator begin() {
        return iterator{ coro };
    }

    std::default_sentinel_t end() {
        return {};
    }
};