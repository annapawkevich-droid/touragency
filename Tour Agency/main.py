from core.container import ServiceContainer

def main():
    container = ServiceContainer()
    booking_service = container.booking_service()
    booking_service.create_booking()

if __name__ == "__main__":
    main()
